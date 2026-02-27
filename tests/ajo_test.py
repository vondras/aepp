#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

import unittest
from unittest.mock import MagicMock, patch

from aepp.connector import TokenResponseError
from aepp.ajo import JourneyOptimizer


def _get_params_from_call(call_args):
    """Extract the params dict from a mock getData call_args, whether passed positionally or as keyword."""
    params = call_args[1].get("params") if call_args[1] else None
    if params is None and len(call_args[0]) > 1:
        params = call_args[0][1]
    return params


def _make_mock_response(status_code: int, body: str, json_data=None):
    """Return a minimal mock resembling a requests.Response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = body
    mock_resp.url = "https://ims-na1.adobelogin.com/ims/token/v3"
    if json_data is not None:
        mock_resp.json.return_value = json_data
    else:
        mock_resp.json.side_effect = ValueError("not json")
    return mock_resp


class TokenPostprocessTest(unittest.TestCase):
    """Unit tests for AdobeRequest._token_postprocess."""

    def _make_connector(self):
        """Return a minimally configured AdobeRequest instance without auth."""
        with patch("aepp.connector.AdobeRequest.__init__", return_value=None):
            from aepp.connector import AdobeRequest
            obj = AdobeRequest.__new__(AdobeRequest)
            obj.config = {
                "token": "",
                "date_limit": 0,
            }
            obj.loggingEnabled = False
            obj.logger = None
            obj.token = None
            return obj

    def test_success_payload_returns_token_info(self):
        """_token_postprocess returns TokenInfo for a valid success response."""
        connector = self._make_connector()
        resp = _make_mock_response(
            200,
            '{"access_token":"tok123","expires_in":86399}',
            json_data={"access_token": "tok123", "expires_in": 86399},
        )
        from aepp.connector import TokenInfo
        result = connector._token_postprocess(resp)
        self.assertIsInstance(result, TokenInfo)
        self.assertEqual(result.token, "tok123")
        self.assertEqual(result.expiry, 86399)

    def test_error_payload_missing_access_token_raises(self):
        """_token_postprocess raises TokenResponseError when access_token is missing."""
        connector = self._make_connector()
        resp = _make_mock_response(
            400,
            '{"error":"invalid_client","error_description":"bad credentials"}',
            json_data={"error": "invalid_client", "error_description": "bad credentials"},
        )
        with self.assertRaises(TokenResponseError) as ctx:
            connector._token_postprocess(resp)
        exc = ctx.exception
        self.assertEqual(exc.status_code, 400)
        self.assertIn("access_token", str(exc))
        self.assertNotIn("bad credentials", str(exc))  # error detail from payload not leaked
        self.assertEqual(exc.endpoint_host, "ims-na1.adobelogin.com")

    def test_error_payload_missing_expires_in_raises(self):
        """_token_postprocess raises TokenResponseError when expires_in is missing."""
        connector = self._make_connector()
        resp = _make_mock_response(
            200,
            '{"access_token":"tok123"}',
            json_data={"access_token": "tok123"},
        )
        with self.assertRaises(TokenResponseError) as ctx:
            connector._token_postprocess(resp)
        exc = ctx.exception
        self.assertEqual(exc.status_code, 200)
        self.assertIn("expires_in", str(exc))

    def test_non_json_response_raises(self):
        """_token_postprocess raises TokenResponseError for non-JSON responses."""
        connector = self._make_connector()
        resp = _make_mock_response(
            503,
            "<html><body>Service Unavailable</body></html>",
        )
        with self.assertRaises(TokenResponseError) as ctx:
            connector._token_postprocess(resp)
        exc = ctx.exception
        self.assertEqual(exc.status_code, 503)
        self.assertIn("non-JSON", str(exc))
        self.assertIn("Service Unavailable", exc.response_snippet)

    def test_error_message_does_not_contain_secrets(self):
        """TokenResponseError message must not expose client secrets."""
        connector = self._make_connector()
        resp = _make_mock_response(
            401,
            '{"error":"unauthorized","client_secret":"s3cr3t"}',
            json_data={"error": "unauthorized", "client_secret": "s3cr3t"},
        )
        with self.assertRaises(TokenResponseError) as ctx:
            connector._token_postprocess(resp)
        exc = ctx.exception
        # The exception message (str(exc)) should not contain the secret value
        self.assertNotIn("s3cr3t", str(exc))
        # The response_snippet may contain raw body for debugging but that is acceptable
        # per spec (bounded snippet); the exception *message* must not.

    def test_token_response_error_attributes(self):
        """TokenResponseError exposes status_code, response_snippet, endpoint_host."""
        exc = TokenResponseError("msg", status_code=401, response_snippet="body", endpoint_host="host.adobe.com")
        self.assertEqual(exc.status_code, 401)
        self.assertEqual(exc.response_snippet, "body")
        self.assertEqual(exc.endpoint_host, "host.adobe.com")


class JourneyOptimizerTest(unittest.TestCase):
    """Unit tests for the JourneyOptimizer AJO client."""

    @patch("aepp.connector.AdobeRequest")
    def test_list_journeys_calls_correct_endpoint(self, mock_connector_cls):
        """list_journeys calls GET /ajo/journey on the AJO base URL."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"results": [], "page": 0, "limit": 100, "pages": 1}

        ajo = JourneyOptimizer()
        result = ajo.list_journeys()

        mock_conn.getData.assert_called_once()
        call_args = mock_conn.getData.call_args
        endpoint_used = call_args[0][0]
        self.assertEqual(endpoint_used, "https://platform.adobe.io/ajo/journey")
        self.assertIn("results", result)

    @patch("aepp.connector.AdobeRequest")
    def test_list_journeys_passes_pagination_params(self, mock_connector_cls):
        """list_journeys forwards page and pageSize query parameters."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"results": [], "page": 2, "limit": 10, "pages": 5}

        ajo = JourneyOptimizer()
        ajo.list_journeys(page=2, page_size=10)

        params_passed = _get_params_from_call(mock_conn.getData.call_args)
        self.assertIsNotNone(params_passed)
        self.assertEqual(params_passed.get("page"), 2)
        self.assertEqual(params_passed.get("pageSize"), 10)

    @patch("aepp.connector.AdobeRequest")
    def test_list_journeys_optional_filter_and_sort(self, mock_connector_cls):
        """list_journeys forwards optional filter, fields, and sort parameters."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"results": [], "page": 0, "limit": 100, "pages": 1}

        ajo = JourneyOptimizer()
        ajo.list_journeys(filter="status=draft", fields="name,status", sort="name=asc")

        params_passed = _get_params_from_call(mock_conn.getData.call_args)
        self.assertEqual(params_passed.get("filter"), "status=draft")
        self.assertEqual(params_passed.get("fields"), "name,status")
        self.assertEqual(params_passed.get("sort"), "name=asc")

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_calls_correct_endpoint(self, mock_connector_cls):
        """get_journey calls GET /ajo/journey/{id}."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"id": "journey-123", "name": "My Journey"}

        ajo = JourneyOptimizer()
        result = ajo.get_journey("journey-123")

        mock_conn.getData.assert_called_once()
        call_args = mock_conn.getData.call_args
        endpoint_used = call_args[0][0]
        self.assertEqual(endpoint_used, "https://platform.adobe.io/ajo/journey/journey-123")
        self.assertEqual(result["id"], "journey-123")

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_with_include_param(self, mock_connector_cls):
        """get_journey forwards the include parameter."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"id": "j1", "campaigns": []}

        ajo = JourneyOptimizer()
        ajo.get_journey("j1", include="campaigns,rulesets")

        params_passed = _get_params_from_call(mock_conn.getData.call_args)
        self.assertEqual(params_passed.get("include"), "campaigns,rulesets")

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_raises_on_empty_id(self, mock_connector_cls):
        """get_journey raises ValueError when journey_id is empty."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}

        ajo = JourneyOptimizer()
        with self.assertRaises(ValueError):
            ajo.get_journey("")

    @patch("aepp.connector.AdobeRequest")
    def test_custom_ajo_base_url_is_used(self, mock_connector_cls):
        """JourneyOptimizer uses ajo_base_url from config when provided."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": "https://custom.ajo.example.com"}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"results": [], "page": 0, "limit": 100, "pages": 1}

        ajo = JourneyOptimizer()
        ajo.list_journeys()

        call_args = mock_conn.getData.call_args
        endpoint_used = call_args[0][0]
        self.assertEqual(endpoint_used, "https://custom.ajo.example.com/ajo/journey")

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_ids_extracts_ids(self, mock_connector_cls):
        """get_journey_ids returns a flat list of journey ID strings."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {
            "results": [{"id": "j1", "name": "Journey 1"}, {"id": "j2", "name": "Journey 2"}],
            "page": 0,
            "limit": 100,
            "pages": 1,
        }

        ajo = JourneyOptimizer()
        ids = ajo.get_journey_ids()

        self.assertEqual(ids, ["j1", "j2"])

    @patch("aepp.connector.AdobeRequest")
    def test_list_journeys_autopaginate(self, mock_connector_cls):
        """list_journeys auto-paginates when n_results exceeds one page."""
        mock_conn = mock_connector_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}

        page0 = {"results": [{"id": "j1"}, {"id": "j2"}], "page": 0, "limit": 2, "pages": 2}
        page1 = {"results": [{"id": "j3"}, {"id": "j4"}], "page": 1, "limit": 2, "pages": 2}
        mock_conn.getData.side_effect = [page0, page1]

        ajo = JourneyOptimizer()
        result = ajo.list_journeys(page_size=2, n_results=4)

        self.assertEqual(len(result["results"]), 4)
        self.assertEqual(mock_conn.getData.call_count, 2)
