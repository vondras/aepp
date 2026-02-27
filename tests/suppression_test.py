#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.suppression import Suppression
import unittest
from unittest.mock import patch


class SuppressionTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_list_addresses(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Suppression()
        result = obj.listAddresses()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_add_addresses(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = [{"id": "addr-1"}]
        obj = Suppression()
        result = obj.addAddresses([{"entity": {"entityValue": "bad@example.com"}}])
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_add_addresses_requires_data(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.addAddresses(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_address(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"email": "bad@example.com"}
        obj = Suppression()
        result = obj.getAddress("bad@example.com")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_address_requires_email(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.getAddress(None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_address(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Suppression()
        result = obj.deleteAddress("bad@example.com")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_address_requires_email(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.deleteAddress(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_domains(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Suppression()
        result = obj.listDomains()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_add_domains(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = [{"id": "dom-1"}]
        obj = Suppression()
        result = obj.addDomains([{"entity": {"entityValue": "baddomain.com"}}])
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_add_domains_requires_data(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.addDomains(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_domain(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"domain": "baddomain.com"}
        obj = Suppression()
        result = obj.getDomain("baddomain.com")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_domain_requires_domain(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.getDomain(None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_domain(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Suppression()
        result = obj.deleteDomain("baddomain.com")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_domain_requires_domain(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.deleteDomain(None)

    @patch("aepp.connector.AdobeRequest")
    def test_list_upload_jobs(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"items": []}
        obj = Suppression()
        result = obj.listUploadJobs()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_upload_job(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"jobId": "job-1"}
        obj = Suppression()
        result = obj.getUploadJob("job-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_upload_job_requires_id(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.getUploadJob(None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_upload_job(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 204
        obj = Suppression()
        result = obj.deleteUploadJob("job-1")
        assert result == 204
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_upload_job_requires_id(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.deleteUploadJob(None)

    @patch("aepp.connector.AdobeRequest")
    def test_delete_all_suppressions(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.deleteData.return_value = 202
        obj = Suppression()
        result = obj.deleteAllSuppressions("org-1", "sandbox-1")
        assert result == 202
        instance_conn.deleteData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_delete_all_suppressions_requires_org_id(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.deleteAllSuppressions(None, "sandbox-1")

    @patch("aepp.connector.AdobeRequest")
    def test_delete_all_suppressions_requires_sandbox_id(self, mock_connector):
        obj = Suppression()
        with self.assertRaises(ValueError):
            obj.deleteAllSuppressions("org-1", None)
