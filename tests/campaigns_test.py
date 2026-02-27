#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.campaigns import Campaigns
import unittest
from unittest.mock import patch


class CampaignsTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaigns(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": [], "count": 0}
        obj = Campaigns()
        result = obj.getCampaigns()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "camp-1"}
        obj = Campaigns()
        result = obj.getCampaign("camp-1")
        assert result["id"] == "camp-1"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_requires_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getCampaign(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_versions(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Campaigns()
        result = obj.getCampaignVersions("camp-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_versions_requires_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getCampaignVersions(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_message(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "msg-1"}
        obj = Campaigns()
        result = obj.getCampaignMessage("camp-1", "msg-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_message_requires_campaign_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getCampaignMessage(None, "msg-1")

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_message_requires_message_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getCampaignMessage("camp-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_message_variant(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "var-1"}
        obj = Campaigns()
        result = obj.getCampaignMessageVariant("camp-1", "msg-1", "email", "var-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_message_variant_requires_all_ids(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getCampaignMessageVariant(None, "msg-1", "email", "var-1")
        with self.assertRaises(ValueError):
            obj.getCampaignMessageVariant("camp-1", None, "email", "var-1")
        with self.assertRaises(ValueError):
            obj.getCampaignMessageVariant("camp-1", "msg-1", None, "var-1")
        with self.assertRaises(ValueError):
            obj.getCampaignMessageVariant("camp-1", "msg-1", "email", None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_publishing_notifications(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Campaigns()
        result = obj.getCampaignPublishingNotifications("camp-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_campaign_package(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "pkg-1"}
        obj = Campaigns()
        result = obj.getCampaignPackage("camp-1", "pkg-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_workflow(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "wf-1"}
        obj = Campaigns()
        result = obj.getWorkflow("wf-1")
        assert result["id"] == "wf-1"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_workflow_requires_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getWorkflow(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_surfaces(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Campaigns()
        result = obj.getSurfaces()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_surface(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"id": "surf-1"}
        obj = Campaigns()
        result = obj.getSurface("email", "surf-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_surface_requires_channel_and_id(self, mock_connector):
        obj = Campaigns()
        with self.assertRaises(ValueError):
            obj.getSurface(None, "surf-1")
        with self.assertRaises(ValueError):
            obj.getSurface("email", None)
