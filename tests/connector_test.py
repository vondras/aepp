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
from aepp.connector import AdobeRequest, TokenError, TokenInfo


class TokenErrorTest(unittest.TestCase):

    def _make_connector(self):
        """Return an AdobeRequest instance with _checkingDate no-op'd."""
        with patch("aepp.connector.AdobeRequest.__init__", return_value=None):
            conn = AdobeRequest.__new__(AdobeRequest)
            conn.token = None
            conn.config = {}
            conn.loggingEnabled = False
            conn.connectionType = "oauthV2"
            return conn

    def test_token_error_raised_on_missing_access_token(self):
        conn = self._make_connector()
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "invalid_client", "error_description": "Bad credentials"}
        with self.assertRaises(TokenError) as ctx:
            conn._token_postprocess(response=mock_response)
        assert "access_token" in str(ctx.exception)

    def test_token_error_raised_on_missing_expires_in(self):
        conn = self._make_connector()
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "some-token"}
        with self.assertRaises(TokenError) as ctx:
            conn._token_postprocess(response=mock_response)
        assert "expires_in" in str(ctx.exception)

    def test_token_error_message_bounded(self):
        conn = self._make_connector()
        long_body = "x" * 500
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": long_body}
        with self.assertRaises(TokenError) as ctx:
            conn._token_postprocess(response=mock_response)
        # The snippet in the message must be ≤200 chars of the response body
        msg = str(ctx.exception)
        # The full 500-char body should NOT appear verbatim
        assert long_body not in msg

    def test_token_info_returned_on_success(self):
        conn = self._make_connector()
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "tok123", "expires_in": 86399}
        result = conn._token_postprocess(response=mock_response)
        assert isinstance(result, TokenInfo)
        assert result.token == "tok123"
        assert result.expiry == 86399

    def test_token_error_raised_on_non_json_response(self):
        conn = self._make_connector()
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_response.text = "<html><body>Bad Gateway</body></html>"
        with self.assertRaises(TokenError) as ctx:
            conn._token_postprocess(response=mock_response)
        assert "non-JSON" in str(ctx.exception)
