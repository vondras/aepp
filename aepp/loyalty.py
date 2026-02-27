#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

## Internal Library
import aepp
from aepp._ajobase import _AJOBase
from typing import Union
from .configs import ConnectObject


class Loyalty(_AJOBase):
    """
    Class to manage Adobe Journey Optimizer Customer Loyalty Challenges.
    Implements the loyalty-challenges.yaml OpenAPI spec (private beta).
    Documentation: https://experienceleague.adobe.com/docs/journey-optimizer/using/loyalty-challenges/get-started.html
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Loyalty class.
        Arguments:
            config : OPTIONAL : config object in the config module. (DO NOT MODIFY)
            header : OPTIONAL : header object in the config module. (DO NOT MODIFY)
            loggingObject : OPTIONAL : logging object to log messages.
        """
        super().__init__(
            config=config, header=header, loggingObject=loggingObject, **kwargs
        )
        self.endpoint = (
            aepp.config.endpoints["global"]
            + aepp.config.endpoints["ajo"]
        )

    # ------------------------------------------------------------------ #
    # Challenge State                                                      #
    # ------------------------------------------------------------------ #

    def signupChallenge(self, challengeId: str, data: dict) -> dict:
        """
        Sign a profile up for a loyalty challenge.
        Implements POST /ajo/loyalty/challenges/signup/{challengeId}
        Arguments:
            challengeId : REQUIRED : The challenge ID.
            data : REQUIRED : Signup payload (profileId, namespace, etc.).
        """
        if challengeId is None:
            raise ValueError("A challenge ID is required.")
        if data is None:
            raise ValueError("A signup payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting signupChallenge for: {challengeId}")
        path = f"/loyalty/challenges/signup/{challengeId}"
        return self.connector.postData(self.endpoint + path, data=data)

    def withdrawChallenge(self, profileId: str, challengeId: str) -> dict:
        """
        Withdraw a profile from a loyalty challenge.
        Implements POST /ajo/loyalty/challenges/{profileId}/withdraw/{challengeId}
        Arguments:
            profileId : REQUIRED : The profile ID.
            challengeId : REQUIRED : The challenge ID.
        """
        if profileId is None:
            raise ValueError("A profile ID is required.")
        if challengeId is None:
            raise ValueError("A challenge ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting withdrawChallenge for profile: {profileId}, challenge: {challengeId}"
            )
        path = f"/loyalty/challenges/{profileId}/withdraw/{challengeId}"
        return self.connector.postData(self.endpoint + path, data={})

    def sendChallengeEvent(self, data: dict) -> dict:
        """
        Send a task event for a loyalty challenge.
        Implements POST /ajo/loyalty/challenges/events
        Arguments:
            data : REQUIRED : Event payload.
        """
        if data is None:
            raise ValueError("An event payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting sendChallengeEvent")
        path = "/loyalty/challenges/events"
        return self.connector.postData(self.endpoint + path, data=data)

    def getProfileChallenges(self, profileId: str, state: str = None) -> dict:
        """
        Retrieve all active challenges for a profile.
        Implements GET /ajo/loyalty/challenges/{profileId}
        Arguments:
            profileId : REQUIRED : The profile ID.
            state : OPTIONAL : Filter by challenge state ("active", "complete").
        """
        if profileId is None:
            raise ValueError("A profile ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getProfileChallenges for: {profileId}")
        path = f"/loyalty/challenges/{profileId}"
        params = {}
        if state is not None:
            params["state"] = state
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getChallengeState(
        self, pid: str, cid: str = None, v: str = None
    ) -> dict:
        """
        Retrieve challenge state for a profile ID.
        Implements GET /ajo/loyalty/challenges/state
        Arguments:
            pid : REQUIRED : Profile ID of the loyalty guest.
            cid : OPTIONAL : Challenge ID (if omitted, all active challenges returned).
            v : OPTIONAL : Response version (default "2").
        """
        if pid is None:
            raise ValueError("A profile ID (pid) is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getChallengeState for pid: {pid}")
        path = "/loyalty/challenges/state"
        params = {"pid": pid}
        if cid is not None:
            params["cid"] = cid
        if v is not None:
            params["v"] = v
        return self.connector.getData(self.endpoint + path, params=params)

    def getOrgChallenges(self) -> dict:
        """
        Retrieve all active challenges for the organization.
        Implements GET /ajo/loyalty/challenges/org
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getOrgChallenges")
        path = "/loyalty/challenges/org"
        return self.connector.getData(self.endpoint + path)

    def getProfileChallengesOD(
        self, id: str, idNS: str = None, v: str = None
    ) -> dict:
        """
        Retrieve all active challenges for a profile (OD variant).
        Implements GET /ajo/loyalty/challenges/od
        Arguments:
            id : REQUIRED : Profile ID of the loyalty guest.
            idNS : OPTIONAL : Namespace for the profile ID.
            v : OPTIONAL : Response version.
        """
        if id is None:
            raise ValueError("A profile ID (id) is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getProfileChallengesOD for id: {id}")
        path = "/loyalty/challenges/od"
        params = {"id": id}
        if idNS is not None:
            params["idNS"] = idNS
        if v is not None:
            params["v"] = v
        return self.connector.getData(self.endpoint + path, params=params)

    def getChallengeHealth(self) -> dict:
        """
        Health check for the loyalty challenges service.
        Implements GET /ajo/loyalty/challenges/health
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getChallengeHealth")
        path = "/loyalty/challenges/health"
        return self.connector.getData(self.endpoint + path)

    def getLiveness(self) -> dict:
        """
        Liveness probe for the loyalty challenges service.
        Implements GET /ajo/actuator/liveness
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getLiveness")
        path = "/actuator/liveness"
        return self.connector.getData(self.endpoint + path)

    def getHealthCheck(self) -> dict:
        """
        Health check probe for the loyalty challenges service.
        Implements GET /ajo/actuator/health
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getHealthCheck")
        path = "/actuator/health"
        return self.connector.getData(self.endpoint + path)
