#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

from copy import deepcopy
from typing import Optional, Union


class JourneyManager:
    """
    Manager for a single Adobe Journey Optimizer journey object.

    Wraps the raw journey dict returned by ``Journey.getJourney``
    and exposes typed helpers for common access patterns (node enumeration,
    status checks, campaign retrieval, etc.).  The manager does not make any
    network calls unless you explicitly call a method that requires one.

    Source spec: ``static/journey-retrieve.yaml``
    (AdobeDocs/journey-optimizer-apis)

    Arguments:
        journey : REQUIRED : Either the journey ID string or the journey dict
                  returned by ``Journey.getJourney``.
        journey_client : OPTIONAL : A ``Journey`` instance.  Required when
                         ``journey`` is an ID string so that the journey
                         definition can be fetched from the API.
        include : OPTIONAL : Comma-separated enrichment keys forwarded to
                  ``Journey.getJourney`` when fetching by ID
                  (e.g. ``"campaigns,rulesets"``).
    """

    def __init__(
        self,
        journey: Union[str, dict],
        journey_client=None,
        include: Optional[str] = None,
    ) -> None:
        if isinstance(journey, dict):
            self._journey = journey
        elif isinstance(journey, str):
            if journey_client is None:
                raise ValueError(
                    "A journey_client instance is required when journey is an ID string."
                )
            self._journey = journey_client.getJourney(journey, include=include)
        else:
            raise TypeError("journey must be a dict or a journey ID string.")

    # ------------------------------------------------------------------
    # Basic properties
    # ------------------------------------------------------------------

    @property
    def id(self) -> Optional[str]:
        """Unique journey ID."""
        return self._journey.get("id")

    @property
    def name(self) -> Optional[str]:
        """Human-readable journey name."""
        return self._journey.get("name")

    @property
    def status(self) -> Optional[str]:
        """Current journey status (e.g. ``"Draft"``, ``"Live"``, ``"Finished"``)."""
        return self._journey.get("status")

    @property
    def sandbox_name(self) -> Optional[str]:
        """Name of the sandbox this journey belongs to."""
        return self._journey.get("sandboxName")

    @property
    def nodes(self) -> list:
        """List of node dicts that make up this journey's graph."""
        return self._journey.get("nodes", [])

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def get_node_ids(self) -> list:
        """Return a flat list of node ID strings present in this journey."""
        return [n.get("id") for n in self.nodes if n.get("id")]

    def get_node(self, node_id: str) -> Optional[dict]:
        """Return the node dict with the given ID, or ``None`` if not found."""
        for node in self.nodes:
            if node.get("id") == node_id:
                return node
        return None

    def get_campaigns(self, journey_client) -> list:
        """
        Return the campaigns linked to this journey.

        Fetches the journey again with ``include=campaigns`` and returns the
        ``campaigns`` list from the enriched response.

        Arguments:
            journey_client : REQUIRED : A ``Journey`` instance.
        """
        if self.id is None:
            raise ValueError("Journey ID is not available; cannot fetch campaigns.")
        enriched = journey_client.getJourney(self.id, include="campaigns")
        return enriched.get("campaigns", [])

    def to_dict(self) -> dict:
        """Return a deep copy of the raw journey definition dict."""
        return deepcopy(self._journey)

    def __str__(self) -> str:
        return f"JourneyManager(id={self.id!r}, name={self.name!r}, status={self.status!r})"

    def __repr__(self) -> str:
        return self.__str__()
