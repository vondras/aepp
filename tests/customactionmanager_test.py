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

from aepp.customactionmanager import CustomActionManager


class CustomActionManagerCappingTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_get_capping_configs_endpoint(self, mock_cls):
        """get_capping_configs calls GET /journey/orchestration/endpointConfigs."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = []

        cam = CustomActionManager()
        cam.get_capping_configs()

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs")

    @patch("aepp.connector.AdobeRequest")
    def test_get_capping_configs_unwraps_dict(self, mock_cls):
        """get_capping_configs extracts items list from a dict response."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"items": [{"uid": "c1"}]}

        cam = CustomActionManager()
        result = cam.get_capping_configs()
        self.assertEqual(result, [{"uid": "c1"}])

    @patch("aepp.connector.AdobeRequest")
    def test_create_capping_config_endpoint(self, mock_cls):
        """create_capping_config calls POST /journey/orchestration/endpointConfigs."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"uid": "new-cap"}

        cam = CustomActionManager()
        cam.create_capping_config({"url": "https://api.example.com", "methods": ["POST"], "services": ["action"], "orgId": "org1"})

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs")

    @patch("aepp.connector.AdobeRequest")
    def test_create_capping_config_raises_on_empty(self, mock_cls):
        """create_capping_config raises ValueError when config_def is empty."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cam = CustomActionManager()
        with self.assertRaises(ValueError):
            cam.create_capping_config({})

    @patch("aepp.connector.AdobeRequest")
    def test_get_capping_config_endpoint(self, mock_cls):
        """get_capping_config calls GET /journey/orchestration/endpointConfigs/{uid}."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"uid": "cap-1"}

        cam = CustomActionManager()
        cam.get_capping_config("cap-1")

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs/cap-1")

    @patch("aepp.connector.AdobeRequest")
    def test_get_capping_config_raises_on_empty_uid(self, mock_cls):
        """get_capping_config raises ValueError for empty uid."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cam = CustomActionManager()
        with self.assertRaises(ValueError):
            cam.get_capping_config("")

    @patch("aepp.connector.AdobeRequest")
    def test_can_deploy_capping_config_endpoint(self, mock_cls):
        """can_deploy_capping_config calls GET /endpointConfigs/canDeploy/{uid}."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"canDeploy": True}

        cam = CustomActionManager()
        cam.can_deploy_capping_config("cap-1")

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs/canDeploy/cap-1")

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_capping_config_endpoint(self, mock_cls):
        """deploy_capping_config calls POST /endpointConfigs/{uid}/deploy."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {}

        cam = CustomActionManager()
        cam.deploy_capping_config("cap-1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs/cap-1/deploy")

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_capping_config_endpoint(self, mock_cls):
        """undeploy_capping_config calls POST /endpointConfigs/{uid}/undeploy."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {}

        cam = CustomActionManager()
        cam.undeploy_capping_config("cap-1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs/cap-1/undeploy")

    @patch("aepp.connector.AdobeRequest")
    def test_delete_capping_config_endpoint(self, mock_cls):
        """delete_capping_config calls DELETE /endpointConfigs/{uid}."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.deleteData.return_value = 200

        cam = CustomActionManager()
        cam.delete_capping_config("cap-1")

        url = mock_conn.deleteData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/endpointConfigs/cap-1")


class CustomActionManagerThrottlingTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_get_throttling_configs_endpoint(self, mock_cls):
        """get_throttling_configs calls GET /journey/orchestration/throttlingConfigs."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = []

        cam = CustomActionManager()
        cam.get_throttling_configs()

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/throttlingConfigs")

    @patch("aepp.connector.AdobeRequest")
    def test_create_throttling_config_endpoint(self, mock_cls):
        """create_throttling_config calls POST /journey/orchestration/throttlingConfigs."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {"uid": "throt-1"}

        cam = CustomActionManager()
        cam.create_throttling_config({"maxThroughput": 100, "urlPattern": "https://api.example.com/*", "methods": ["POST"]})

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/throttlingConfigs")

    @patch("aepp.connector.AdobeRequest")
    def test_get_throttling_config_endpoint(self, mock_cls):
        """get_throttling_config calls GET /journey/orchestration/throttlingConfigs/{uid}."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = {"uid": "throt-1"}

        cam = CustomActionManager()
        cam.get_throttling_config("throt-1")

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/throttlingConfigs/throt-1")

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_throttling_config_endpoint(self, mock_cls):
        """deploy_throttling_config calls POST /throttlingConfigs/{uid}/deploy."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {}

        cam = CustomActionManager()
        cam.deploy_throttling_config("throt-1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/throttlingConfigs/throt-1/deploy")

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_throttling_config_endpoint(self, mock_cls):
        """undeploy_throttling_config calls POST /throttlingConfigs/{uid}/undeploy."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.postData.return_value = {}

        cam = CustomActionManager()
        cam.undeploy_throttling_config("throt-1")

        url = mock_conn.postData.call_args[0][0]
        self.assertEqual(url, "https://platform.adobe.io/journey/orchestration/throttlingConfigs/throt-1/undeploy")

    @patch("aepp.connector.AdobeRequest")
    def test_delete_throttling_config_raises_on_empty_uid(self, mock_cls):
        """delete_throttling_config raises ValueError for empty uid."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": None}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        cam = CustomActionManager()
        with self.assertRaises(ValueError):
            cam.delete_throttling_config("")

    @patch("aepp.connector.AdobeRequest")
    def test_custom_ajo_base_url_used(self, mock_cls):
        """CustomActionManager uses ajo_base_url from config when set."""
        mock_conn = mock_cls.return_value
        mock_conn.config = {"sandbox": "prod", "ajo_base_url": "https://custom.ajo.example.com"}
        mock_conn.header = {}
        mock_conn.endpoints = {"global": "https://platform.adobe.io"}
        mock_conn.getData.return_value = []

        cam = CustomActionManager()
        cam.get_throttling_configs()

        url = mock_conn.getData.call_args[0][0]
        self.assertEqual(url, "https://custom.ajo.example.com/journey/orchestration/throttlingConfigs")
