#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from aepp.loyalty import Loyalty
import unittest
from unittest.mock import patch


class LoyaltyTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_signup_challenge(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Loyalty()
        result = obj.signupChallenge("chal-1", {"profileId": "p1"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_signup_challenge_requires_challenge_id(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.signupChallenge(None, {"profileId": "p1"})

    @patch("aepp.connector.AdobeRequest")
    def test_signup_challenge_requires_data(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.signupChallenge("chal-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_withdraw_challenge(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Loyalty()
        result = obj.withdrawChallenge("prof-1", "chal-1")
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_withdraw_challenge_requires_profile_id(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.withdrawChallenge(None, "chal-1")

    @patch("aepp.connector.AdobeRequest")
    def test_withdraw_challenge_requires_challenge_id(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.withdrawChallenge("prof-1", None)

    @patch("aepp.connector.AdobeRequest")
    def test_send_challenge_event(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.postData.return_value = {}
        obj = Loyalty()
        result = obj.sendChallengeEvent({"event": "task_completed"})
        assert result is not None
        instance_conn.postData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_send_challenge_event_requires_data(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.sendChallengeEvent(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_profile_challenges(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"challenges": []}
        obj = Loyalty()
        result = obj.getProfileChallenges("prof-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_profile_challenges_requires_profile_id(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.getProfileChallenges(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_challenge_state(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"challenges": []}
        obj = Loyalty()
        result = obj.getChallengeState("prof-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_challenge_state_requires_pid(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.getChallengeState(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_org_challenges(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"challenges": []}
        obj = Loyalty()
        result = obj.getOrgChallenges()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_profile_challenges_od(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"challenges": []}
        obj = Loyalty()
        result = obj.getProfileChallengesOD("prof-1")
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_profile_challenges_od_requires_id(self, mock_connector):
        obj = Loyalty()
        with self.assertRaises(ValueError):
            obj.getProfileChallengesOD(None)

    @patch("aepp.connector.AdobeRequest")
    def test_get_challenge_health(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = {"status": "ok"}
        obj = Loyalty()
        result = obj.getChallengeHealth()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_liveness(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = "UP"
        obj = Loyalty()
        result = obj.getLiveness()
        assert result is not None
        instance_conn.getData.assert_called_once()

    @patch("aepp.connector.AdobeRequest")
    def test_get_health_check(self, mock_connector):
        instance_conn = mock_connector.return_value
        instance_conn.getData.return_value = "UP"
        obj = Loyalty()
        result = obj.getHealthCheck()
        assert result is not None
        instance_conn.getData.assert_called_once()
