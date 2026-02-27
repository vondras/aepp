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
from unittest.mock import patch
from aepp._ajobase import create_ajo_client
from aepp.journey import Journey
from aepp.content import Content
from aepp.orchestration import Orchestration


class AJOBaseTest(unittest.TestCase):

    @patch("aepp.connector.AdobeRequest")
    def test_factory_journey(self, mock_connector):
        obj = create_ajo_client("journey")
        assert isinstance(obj, Journey)

    @patch("aepp.connector.AdobeRequest")
    def test_factory_content(self, mock_connector):
        obj = create_ajo_client("content")
        assert isinstance(obj, Content)

    @patch("aepp.connector.AdobeRequest")
    def test_factory_orchestration(self, mock_connector):
        obj = create_ajo_client("orchestration")
        assert isinstance(obj, Orchestration)

    @patch("aepp.connector.AdobeRequest")
    def test_factory_case_insensitive(self, mock_connector):
        obj = create_ajo_client("Journey")
        assert isinstance(obj, Journey)

    @patch("aepp.connector.AdobeRequest")
    def test_factory_unknown_service_raises(self, mock_connector):
        with self.assertRaises(ValueError):
            create_ajo_client("unknown")

    @patch("aepp.connector.AdobeRequest")
    def test_class_names(self, mock_connector):
        journey = Journey()
        content = Content()
        orchestration = Orchestration()
        assert type(journey).__name__ == "Journey"
        assert type(content).__name__ == "Content"
        assert type(orchestration).__name__ == "Orchestration"
