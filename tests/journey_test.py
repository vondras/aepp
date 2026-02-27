#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.journey import Journey
import unittest
from unittest.mock import patch, MagicMock


class JourneyTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_get_journeys_returns_result(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"results": [], "page": 0, "limit": 100, "pages": 1}
        obj = Journey()
        result = obj.getJourneys()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_journeys_with_params(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"results": [], "page": 1, "limit": 20, "pages": 1}
        obj = Journey()
        result = obj.getJourneys(filter="status=draft", page=1, pageSize=20, fields="name,status", sort="name=asc")
        assert result is not None
        call_kwargs = instance_conn.getData.call_args
        params = call_kwargs[1].get("params") or call_kwargs[0][1]
        assert params["filter"] == "status=draft"
        assert params["page"] == 1
        assert params["pageSize"] == 20

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_by_id(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "test-id", "name": "My Journey"}
        obj = Journey()
        result = obj.getJourney("test-id")
        assert result is not None
        assert result["id"] == "test-id"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_by_id_with_include(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "test-id"}
        obj = Journey()
        result = obj.getJourney("test-id", include="campaigns,rulesets")
        assert result is not None
        call_kwargs = instance_conn.getData.call_args
        params = call_kwargs[1].get("params") or call_kwargs[0][1]
        assert params["include"] == "campaigns,rulesets"

    @patch("aepp.connector.AdobeRequest")
    def test_get_journey_requires_id(self, mock_connector):
        obj = Journey()
        with self.assertRaises(ValueError):
            obj.getJourney(None)
