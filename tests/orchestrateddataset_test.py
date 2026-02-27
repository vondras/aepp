#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.orchestrateddataset import OrchestratedDataset
import unittest
from unittest.mock import patch


class OrchestratedDatasetTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_validate_dataset_extension(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"valid": True}
        obj = OrchestratedDataset()
        result = obj.validateDatasetExtension("ds-1")
        assert result is not None
        assert result["valid"] is True
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_validate_dataset_extension_requires_id(self, mock_connector):
        obj = OrchestratedDataset()
        with self.assertRaises(ValueError):
            obj.validateDatasetExtension(None)

    @patch("aepp.connector.AdobeRequest")
    def test_enable_dataset_extension(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = [{"jobId": "job-1"}]
        obj = OrchestratedDataset()
        result = obj.enableDatasetExtension({"datasetId": "ds-1"})
        assert result is not None
        assert result[0]["jobId"] == "job-1"
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_enable_dataset_extension_requires_data(self, mock_connector):
        obj = OrchestratedDataset()
        with self.assertRaises(ValueError):
            obj.enableDatasetExtension(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_dataset_extension_job(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"jobId": "job-1", "status": "COMPLETED"}
        obj = OrchestratedDataset()
        result = obj.getDatasetExtensionJob("job-1")
        assert result is not None
        assert result["status"] == "COMPLETED"
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_dataset_extension_job_requires_id(self, mock_connector):
        obj = OrchestratedDataset()
        with self.assertRaises(ValueError):
            obj.getDatasetExtensionJob(None)
