#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.simulations import Simulations
import unittest
from unittest.mock import patch


class SimulationsTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_campaign_proof(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"proofJobId": "pj-1", "status": "CREATED"}
        obj = Simulations()
        result = obj.triggerCampaignProof("camp-1", {"recipients": []})
        assert result is not None
        assert result["proofJobId"] == "pj-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_campaign_proof_requires_campaign_id(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.triggerCampaignProof(None, {"recipients": []})

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_campaign_proof_requires_data(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.triggerCampaignProof("camp-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_proof_status(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"proofJobId": "pj-1", "status": "SUBMITTED"}
        obj = Simulations()
        result = obj.getCampaignProofStatus("camp-1", "pj-1")
        assert result is not None
        assert result["status"] == "SUBMITTED"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_proof_status_requires_campaign_id(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.getCampaignProofStatus(None, "pj-1")

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_proof_status_requires_proof_job_id(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.getCampaignProofStatus("camp-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_create_campaign_preview(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"previews": []}
        obj = Simulations()
        result = obj.createCampaignPreview("camp-1", {"previewRequestItems": []})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_create_campaign_preview_requires_campaign_id(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.createCampaignPreview(None, {"previewRequestItems": []})

    @patch("aepp.connector.AdobeRequest")
    def test_create_campaign_preview_requires_data(self, mock_connector):
        obj = Simulations()
        with self.assertRaises(ValueError):
            obj.createCampaignPreview("camp-1", None)
