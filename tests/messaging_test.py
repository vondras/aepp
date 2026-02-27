#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.messaging import Messaging
import unittest
from unittest.mock import patch


class MessagingTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_unitary_execution(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"executionId": "exec-1"}
        obj = Messaging()
        result = obj.triggerUnitaryExecution({"campaignId": "camp-1"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_unitary_execution_requires_data(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.triggerUnitaryExecution(None)

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_audience_execution(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"executionId": "exec-2"}
        obj = Messaging()
        result = obj.triggerAudienceExecution({"campaignId": "camp-1"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_audience_execution_requires_data(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.triggerAudienceExecution(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_audience_execution_status(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"status": "COMPLETED"}
        obj = Messaging()
        result = obj.getAudienceExecutionStatus("exec-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_audience_execution_status_requires_id(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.getAudienceExecutionStatus(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_scheduled_execution_status(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"status": "SCHEDULED"}
        obj = Messaging()
        result = obj.getScheduledExecutionStatus("sched-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_scheduled_execution_status_requires_id(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.getScheduledExecutionStatus(None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_scheduled_execution(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 200
        obj = Messaging()
        result = obj.deleteScheduledExecution("sched-1")
        assert result == 200
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_scheduled_execution_requires_id(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.deleteScheduledExecution(None)

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_high_throughput_execution(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {"executionId": "exec-3"}
        obj = Messaging()
        result = obj.triggerHighThroughputExecution({"campaignId": "camp-1"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_trigger_high_throughput_execution_requires_data(self, mock_connector):
        obj = Messaging()
        with self.assertRaises(ValueError):
            obj.triggerHighThroughputExecution(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_health(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"status": "UP"}
        obj = Messaging()
        result = obj.getHealth()
        assert result is not None
        instance_conn.getData.assert_called_once()
