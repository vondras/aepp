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


class Simulations(_AJOBase):
    """
    Class to manage Adobe Journey Optimizer Campaign Proofs and Previews.
    Implements the simulations.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/en/docs/journey-optimizer/using/campaigns/review-activate-campaign
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Simulations class.
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
            + aepp.config.endpoints["ajo_simulations"]
        )

    # ------------------------------------------------------------------ #
    # Campaign Proof API                                                   #
    # ------------------------------------------------------------------ #

    def triggerCampaignProof(self, campaignId: str, data: dict) -> dict:
        """
        Trigger a campaign proof job.
        Implements POST /ajo/simulations/campaigns/{campaignId}/proofs
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            data : REQUIRED : Proof job request payload (recipients, etc.).
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if data is None:
            raise ValueError("A proof job request payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting triggerCampaignProof for: {campaignId}")
        path = f"/campaigns/{campaignId}/proofs"
        return self.connector.postData(self.endpoint + path, data=data)

    def getCampaignProofStatus(self, campaignId: str, proofJobId: str) -> dict:
        """
        Get the status of a campaign proof job.
        Implements GET /ajo/simulations/campaigns/{campaignId}/proofs/{proofJobId}
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            proofJobId : REQUIRED : The proof job ID.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if proofJobId is None:
            raise ValueError("A proof job ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getCampaignProofStatus for campaign: {campaignId}, job: {proofJobId}"
            )
        path = f"/campaigns/{campaignId}/proofs/{proofJobId}"
        return self.connector.getData(self.endpoint + path)

    # ------------------------------------------------------------------ #
    # Campaign Preview API                                                 #
    # ------------------------------------------------------------------ #

    def createCampaignPreview(self, campaignId: str, data: dict) -> dict:
        """
        Generate a campaign preview for specified profiles.
        Implements POST /ajo/simulations/campaigns/{campaignId}/previews
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            data : REQUIRED : Preview request payload (previewRequestItems, etc.).
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if data is None:
            raise ValueError("A preview request payload is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting createCampaignPreview for: {campaignId}"
            )
        path = f"/campaigns/{campaignId}/previews"
        return self.connector.postData(self.endpoint + path, data=data)
