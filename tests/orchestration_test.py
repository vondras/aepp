#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.orchestration import Orchestration
import unittest
from unittest.mock import patch, MagicMock


class OrchestrationTest(unittest.TestCase):

    # ------------------------------------------------------------------ #
    # Capping (endpoint) configurations                                   #
    # ------------------------------------------------------------------ #

    @patch("aepp.connector.AdobeRequest")
    def test_create_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"uid": "cfg-1"}
        obj = Orchestration()
        result = obj.createEndpointConfig({"url": "https://example.com", "methods": ["GET"], "services": ["action"], "orgId": "org"})
        assert result is not None
        assert result["uid"] == "cfg-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_create_endpoint_config_requires_data(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.createEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"uid": "cfg-1"}
        obj = Orchestration()
        result = obj.getEndpointConfig("cfg-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.getEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_put_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.putData.return_value = {"uid": "cfg-1"}
        obj = Orchestration()
        result = obj.putEndpointConfig("cfg-1", {"url": "https://example.com"})
        assert result is not None
        instance_conn.putData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_put_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.putEndpointConfig(None, {})

    @patch("aepp.connector.AdobeRequest")
    def test_put_endpoint_config_requires_data(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.putEndpointConfig("cfg-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Orchestration()
        result = obj.deleteEndpointConfig("cfg-1")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.deleteEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_can_deploy_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"canDeploy": True}
        obj = Orchestration()
        result = obj.canDeployEndpointConfig("cfg-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_can_deploy_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.canDeployEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Orchestration()
        result = obj.deployEndpointConfig("cfg-1")
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.deployEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_endpoint_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Orchestration()
        result = obj.undeployEndpointConfig("cfg-1")
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_endpoint_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.undeployEndpointConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_endpoint_configs(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"items": []}
        obj = Orchestration()
        result = obj.listEndpointConfigs()
        assert result is not None
        instance_conn.postData.assert_called_once()

    # ------------------------------------------------------------------ #
    # Throttling configurations                                            #
    # ------------------------------------------------------------------ #

    @patch("aepp.connector.AdobeRequest")
    def test_create_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"uid": "thr-1"}
        obj = Orchestration()
        result = obj.createThrottlingConfig({"maxThroughput": 100, "urlPattern": "https://example.com", "methods": ["POST"]})
        assert result is not None
        assert result["uid"] == "thr-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_create_throttling_config_requires_data(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.createThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"uid": "thr-1"}
        obj = Orchestration()
        result = obj.getThrottlingConfig("thr-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.getThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_put_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.putData.return_value = {"uid": "thr-1"}
        obj = Orchestration()
        result = obj.putThrottlingConfig("thr-1", {"maxThroughput": 200})
        assert result is not None
        instance_conn.putData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_put_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.putThrottlingConfig(None, {})

    @patch("aepp.connector.AdobeRequest")
    def test_put_throttling_config_requires_data(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.putThrottlingConfig("thr-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Orchestration()
        result = obj.deleteThrottlingConfig("thr-1")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.deleteThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_can_deploy_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"canDeploy": True}
        obj = Orchestration()
        result = obj.canDeployThrottlingConfig("thr-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_can_deploy_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.canDeployThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Orchestration()
        result = obj.deployThrottlingConfig("thr-1")
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_deploy_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.deployThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_throttling_config(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Orchestration()
        result = obj.undeployThrottlingConfig("thr-1")
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_undeploy_throttling_config_requires_uid(self, mock_connector):
        obj = Orchestration()
        with self.assertRaises(ValueError):
            obj.undeployThrottlingConfig(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_throttling_configs(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"items": []}
        obj = Orchestration()
        result = obj.listThrottlingConfigs()
        assert result is not None
        instance_conn.postData.assert_called_once()
