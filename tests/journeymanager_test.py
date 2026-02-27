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

from aepp.journeymanager import JourneyManager

_JOURNEY = {
    "id": "j-001",
    "name": "My Journey",
    "status": "Live",
    "sandboxName": "prod",
    "nodes": [
        {"id": "node-1", "type": "entryEvent"},
        {"id": "node-2", "type": "action"},
    ],
    "campaigns": [{"id": "c-1"}],
}


class JourneyManagerTest(unittest.TestCase):

    def test_init_with_dict(self):
        """JourneyManager accepts a raw dict and exposes basic properties."""
        jm = JourneyManager(_JOURNEY)
        self.assertEqual(jm.id, "j-001")
        self.assertEqual(jm.name, "My Journey")
        self.assertEqual(jm.status, "Live")
        self.assertEqual(jm.sandbox_name, "prod")

    def test_init_with_id_requires_optimizer(self):
        """JourneyManager raises ValueError when given an ID without a journey_client."""
        with self.assertRaises(ValueError):
            JourneyManager("j-001")

    def test_init_with_id_fetches_journey(self):
        """JourneyManager calls journey_client.getJourney when given an ID string."""
        mock_client = MagicMock()
        mock_client.getJourney.return_value = _JOURNEY
        jm = JourneyManager("j-001", journey_client=mock_client)
        mock_client.getJourney.assert_called_once_with("j-001", include=None)
        self.assertEqual(jm.name, "My Journey")

    def test_init_with_id_passes_include(self):
        """JourneyManager forwards the include parameter to getJourney."""
        mock_client = MagicMock()
        mock_client.getJourney.return_value = _JOURNEY
        JourneyManager("j-001", journey_client=mock_client, include="campaigns")
        mock_client.getJourney.assert_called_once_with("j-001", include="campaigns")

    def test_init_bad_type_raises(self):
        """JourneyManager raises TypeError for unexpected journey argument type."""
        with self.assertRaises(TypeError):
            JourneyManager(42)

    def test_nodes_property(self):
        """nodes returns the list of node dicts."""
        jm = JourneyManager(_JOURNEY)
        self.assertEqual(len(jm.nodes), 2)

    def test_get_node_ids(self):
        """get_node_ids returns a flat list of all node IDs."""
        jm = JourneyManager(_JOURNEY)
        self.assertEqual(jm.get_node_ids(), ["node-1", "node-2"])

    def test_get_node_found(self):
        """get_node returns the matching node dict."""
        jm = JourneyManager(_JOURNEY)
        node = jm.get_node("node-2")
        self.assertIsNotNone(node)
        self.assertEqual(node["type"], "action")

    def test_get_node_not_found(self):
        """get_node returns None when the ID is not present."""
        jm = JourneyManager(_JOURNEY)
        self.assertIsNone(jm.get_node("nonexistent"))

    def test_get_campaigns(self):
        """get_campaigns calls getJourney with include=campaigns and returns the list."""
        mock_client = MagicMock()
        mock_client.getJourney.return_value = {"id": "j-001", "campaigns": [{"id": "c-1"}]}
        jm = JourneyManager(_JOURNEY)
        result = jm.get_campaigns(mock_client)
        mock_client.getJourney.assert_called_once_with("j-001", include="campaigns")
        self.assertEqual(result, [{"id": "c-1"}])

    def test_get_campaigns_no_id_raises(self):
        """get_campaigns raises ValueError when journey has no id."""
        mock_client = MagicMock()
        jm = JourneyManager({"name": "no-id"})
        with self.assertRaises(ValueError):
            jm.get_campaigns(mock_client)

    def test_to_dict_is_copy(self):
        """to_dict returns a deep copy (mutating it does not affect the manager)."""
        jm = JourneyManager(_JOURNEY)
        d = jm.to_dict()
        d["status"] = "MUTATED"
        self.assertEqual(jm.status, "Live")

    def test_repr(self):
        """__repr__ includes id, name, status."""
        jm = JourneyManager(_JOURNEY)
        r = repr(jm)
        self.assertIn("j-001", r)
        self.assertIn("My Journey", r)
        self.assertIn("Live", r)
