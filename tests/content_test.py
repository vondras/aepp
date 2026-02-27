#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.content import Content
import unittest
from unittest.mock import patch, MagicMock


class ContentTest(unittest.TestCase):

    # ------------------------------------------------------------------ #
    # Templates                                                            #
    # ------------------------------------------------------------------ #

    @patch("aepp.connector.AdobeRequest")
    def test_create_template(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"id": "tmpl-1"}
        obj = Content()
        result = obj.createTemplate({"name": "My Template"})
        assert result is not None
        assert result["id"] == "tmpl-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_create_template_requires_data(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.createTemplate(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_templates(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": [], "count": 0}
        obj = Content()
        result = obj.listTemplates()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_template(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "tmpl-1", "name": "My Template"}
        obj = Content()
        result = obj.getTemplate("tmpl-1")
        assert result is not None
        assert result["id"] == "tmpl-1"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_template_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.getTemplate(None)

    @patch("aepp.connector.AdobeRequest")
    def test_put_template(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.putData.return_value = {}
        obj = Content()
        result = obj.putTemplate("tmpl-1", {"name": "Updated"})
        assert result is not None
        instance_conn.putData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_put_template_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.putTemplate(None, {"name": "x"})

    @patch("aepp.connector.AdobeRequest")
    def test_put_template_requires_data(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.putTemplate("tmpl-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_template(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Content()
        result = obj.deleteTemplate("tmpl-1")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_template_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.deleteTemplate(None)

    @patch("aepp.connector.AdobeRequest")
    def test_patch_template(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.patchData.return_value = {}
        obj = Content()
        ops = [{"op": "replace", "path": "/name", "value": "New Name"}]
        result = obj.patchTemplate("tmpl-1", ops)
        assert result is not None
        instance_conn.patchData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_patch_template_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.patchTemplate(None, [])

    @patch("aepp.connector.AdobeRequest")
    def test_patch_template_requires_operations(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.patchTemplate("tmpl-1", None)

    # ------------------------------------------------------------------ #
    # Fragments                                                            #
    # ------------------------------------------------------------------ #

    @patch("aepp.connector.AdobeRequest")
    def test_create_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"id": "frag-1"}
        obj = Content()
        result = obj.createFragment({"name": "My Fragment"})
        assert result is not None
        assert result["id"] == "frag-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_create_fragment_requires_data(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.createFragment(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_fragments(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": [], "count": 0}
        obj = Content()
        result = obj.listFragments()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "frag-1"}
        obj = Content()
        result = obj.getFragment("frag-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_fragment_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.getFragment(None)

    @patch("aepp.connector.AdobeRequest")
    def test_put_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.putData.return_value = {}
        obj = Content()
        result = obj.putFragment("frag-1", {"name": "Updated"})
        assert result is not None
        instance_conn.putData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_put_fragment_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.putFragment(None, {})

    @patch("aepp.connector.AdobeRequest")
    def test_put_fragment_requires_data(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.putFragment("frag-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_patch_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.patchData.return_value = {}
        obj = Content()
        ops = [{"op": "replace", "path": "/name", "value": "New Name"}]
        result = obj.patchFragment("frag-1", ops)
        assert result is not None
        instance_conn.patchData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_patch_fragment_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.patchFragment(None, [])

    @patch("aepp.connector.AdobeRequest")
    def test_patch_fragment_requires_operations(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.patchFragment("frag-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_publish_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"status": "published"}
        obj = Content()
        result = obj.publishFragment({"fragmentId": "frag-1"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_publish_fragment_requires_data(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.publishFragment(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_live_fragment(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "frag-1", "live": True}
        obj = Content()
        result = obj.getLiveFragment("frag-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_live_fragment_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.getLiveFragment(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_last_publication_status(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"status": "published"}
        obj = Content()
        result = obj.getLastPublicationStatus("frag-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_last_publication_status_requires_id(self, mock_connector):
        obj = Content()
        with self.assertRaises(ValueError):
            obj.getLastPublicationStatus(None)
