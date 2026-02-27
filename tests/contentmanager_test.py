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

from aepp.contentmanager import ContentManager, _MEDIA_TYPE_TEMPLATE, _MEDIA_TYPE_FRAGMENT


def _make_cm():
    """Return a ContentManager with a mocked AdobeRequest connector."""
    with patch("aepp.connector.AdobeRequest") as mock_cls:
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cm = ContentManager()
        cm.connector = mock_conn
        cm.header = {}
        cm.ajoBaseUrl = "https://platform.adobe.io"
    return cm, mock_conn


class ContentManagerTemplateTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_list_templates_endpoint(self, mock_cls):
        """list_templates calls GET /ajo/content/templates."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"items": [], "_links": {}}

        cm = ContentManager()
        result = cm.list_templates()

        mock_conn.getData.assert_called_once()
        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/templates")
        self.assertIn("items", result)

    @patch("aepp.connector.AdobeRequest")
    def test_list_templates_passes_params(self, mock_cls):
        """list_templates forwards pagination and filter params."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"items": []}

        cm = ContentManager()
        cm.list_templates(order_by="modifiedAt=desc", limit=10, start="tok123", property="templateType==html")

        params = mock_conn.getData.call_args[1].get("params") or mock_conn.getData.call_args[0][1]
        self.assertEqual(params.get("orderBy"), "modifiedAt=desc")
        self.assertEqual(params.get("limit"), 10)
        self.assertEqual(params.get("start"), "tok123")
        self.assertEqual(params.get("property"), "templateType==html")

    @patch("aepp.connector.AdobeRequest")
    def test_get_template_endpoint_and_accept_header(self, mock_cls):
        """get_template calls GET /ajo/content/templates/{id} with correct Accept header."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"id": "t1"}

        cm = ContentManager()
        cm.get_template("t1")

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/templates/t1")
        headers_passed = mock_conn.getData.call_args[1].get("headers") or {}
        self.assertEqual(headers_passed.get("Accept"), _MEDIA_TYPE_TEMPLATE)

    @patch("aepp.connector.AdobeRequest")
    def test_get_template_raises_on_empty_id(self, mock_cls):
        """get_template raises ValueError for empty template_id."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cm = ContentManager()
        with self.assertRaises(ValueError):
            cm.get_template("")

    @patch("aepp.connector.AdobeRequest")
    def test_create_template_sets_content_type(self, mock_cls):
        """create_template sends POST with vendor Content-Type header."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"id": "t-new"}

        cm = ContentManager()
        cm.create_template({"name": "My Template", "templateType": "html"})

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/templates")
        headers_passed = mock_conn.postData.call_args[1].get("headers") or {}
        self.assertEqual(headers_passed.get("Content-Type"), _MEDIA_TYPE_TEMPLATE)

    @patch("aepp.connector.AdobeRequest")
    def test_update_template_sends_etag(self, mock_cls):
        """update_template includes If-Match header when etag is provided."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.putData.return_value = {}

        cm = ContentManager()
        cm.update_template("t1", {"name": "Updated"}, etag="v2")

        headers_passed = mock_conn.putData.call_args[1].get("headers") or {}
        self.assertEqual(headers_passed.get("If-Match"), "v2")

    @patch("aepp.connector.AdobeRequest")
    def test_delete_template_endpoint(self, mock_cls):
        """delete_template calls DELETE /ajo/content/templates/{id}."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.deleteData.return_value = 204

        cm = ContentManager()
        cm.delete_template("t1")

        url = mock_conn.deleteData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/templates/t1")

    @patch("aepp.connector.AdobeRequest")
    def test_validate_template_endpoint(self, mock_cls):
        """validate_template calls POST /ajo/content/templates/{id}/validate."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"status": "valid"}

        cm = ContentManager()
        cm.validate_template("t1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/templates/t1/validate")


class ContentManagerFragmentTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_list_fragments_endpoint(self, mock_cls):
        """list_fragments calls GET /ajo/content/fragments."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"items": []}

        cm = ContentManager()
        cm.list_fragments()

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/fragments")

    @patch("aepp.connector.AdobeRequest")
    def test_get_fragment_accept_header(self, mock_cls):
        """get_fragment uses the fragment vendor Accept header."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"id": "f1"}

        cm = ContentManager()
        cm.get_fragment("f1")

        headers_passed = mock_conn.getData.call_args[1].get("headers") or {}
        self.assertEqual(headers_passed.get("Accept"), _MEDIA_TYPE_FRAGMENT)

    @patch("aepp.connector.AdobeRequest")
    def test_create_fragment_content_type(self, mock_cls):
        """create_fragment uses the fragment vendor Content-Type header."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"id": "f-new"}

        cm = ContentManager()
        cm.create_fragment({"name": "My Fragment"})

        headers_passed = mock_conn.postData.call_args[1].get("headers") or {}
        self.assertEqual(headers_passed.get("Content-Type"), _MEDIA_TYPE_FRAGMENT)

    @patch("aepp.connector.AdobeRequest")
    def test_publish_fragment_endpoint(self, mock_cls):
        """publish_fragment calls POST /ajo/content/fragments/{id}/publish."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"id": "f1", "status": "published"}

        cm = ContentManager()
        cm.publish_fragment("f1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/ajo/content/fragments/f1/publish")

    @patch("aepp.connector.AdobeRequest")
    def test_delete_fragment_raises_on_empty_id(self, mock_cls):
        """delete_fragment raises ValueError for empty fragment_id."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cm = ContentManager()
        with self.assertRaises(ValueError):
            cm.delete_fragment("")

    @patch("aepp.connector.AdobeRequest")
    def test_custom_ajo_base_url_used(self, mock_cls):
        """ContentManager uses ajo_base_url from config when set."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": "https://custom.ajo.example.com"}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"items": []}

        cm = ContentManager()
        cm.list_templates()

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://custom.ajo.example.com/ajo/content/templates")
