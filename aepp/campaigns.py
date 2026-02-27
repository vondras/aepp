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


class Campaigns(_AJOBase):
    """
    Class to retrieve and manage Adobe Journey Optimizer Action Campaigns.
    Implements the campaigns-retrieve.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/en/docs/journey-optimizer/using/campaigns/get-started-with-campaigns
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Campaigns class.
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
            + aepp.config.endpoints["ajo_campaigns"]
        )

    # ------------------------------------------------------------------ #
    # Campaign Resource                                                    #
    # ------------------------------------------------------------------ #

    def getCampaigns(
        self,
        count: int = None,
        page: int = None,
        orderby: str = None,
        property: str = None,
        full: bool = None,
        actions: bool = None,
    ) -> dict:
        """
        Retrieve a list of campaigns.
        Implements GET /journey/campaigns/service/campaigns
        Arguments:
            count : OPTIONAL : Number of results per page (default 50).
            page : OPTIONAL : Page number for pagination.
            orderby : OPTIONAL : Sort field (default "name").
            property : OPTIONAL : FIQL filter expression.
            full : OPTIONAL : Whether to include full campaign details.
            actions : OPTIONAL : Whether to include campaign actions (default True).
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getCampaigns")
        path = "/service/campaigns"
        params = {}
        if count is not None:
            params["count"] = count
        if page is not None:
            params["page"] = page
        if orderby is not None:
            params["orderby"] = orderby
        if property is not None:
            params["property"] = property
        if full is not None:
            params["full"] = full
        if actions is not None:
            params["actions"] = actions
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getCampaign(self, campaignId: str) -> dict:
        """
        Retrieve a single campaign by ID.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}
        Arguments:
            campaignId : REQUIRED : The campaign ID.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getCampaign with id: {campaignId}")
        path = f"/service/campaigns/{campaignId}"
        return self.connector.getData(self.endpoint + path)

    def getCampaignVersions(
        self,
        campaignId: str,
        count: int = None,
        page: int = None,
        orderby: str = None,
        property: str = None,
        full: bool = None,
        actions: bool = None,
    ) -> dict:
        """
        Retrieve the versions of a campaign.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}/versions
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            count : OPTIONAL : Number of results per page (default 50).
            page : OPTIONAL : Page number for pagination.
            orderby : OPTIONAL : Sort field (default "name").
            property : OPTIONAL : FIQL filter expression.
            full : OPTIONAL : Whether to include full campaign details.
            actions : OPTIONAL : Whether to include campaign actions.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getCampaignVersions for: {campaignId}")
        path = f"/service/campaigns/{campaignId}/versions"
        params = {}
        if count is not None:
            params["count"] = count
        if page is not None:
            params["page"] = page
        if orderby is not None:
            params["orderby"] = orderby
        if property is not None:
            params["property"] = property
        if full is not None:
            params["full"] = full
        if actions is not None:
            params["actions"] = actions
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getCampaignMessage(self, campaignId: str, messageId: str) -> dict:
        """
        Retrieve a campaign message by ID.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}/messages/{messageId}
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            messageId : REQUIRED : The message ID.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if messageId is None:
            raise ValueError("A message ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getCampaignMessage for campaign: {campaignId}, message: {messageId}"
            )
        path = f"/service/campaigns/{campaignId}/messages/{messageId}"
        return self.connector.getData(self.endpoint + path)

    def getCampaignMessageVariant(
        self, campaignId: str, messageId: str, channel: str, variantId: str
    ) -> dict:
        """
        Retrieve a specific variant of a campaign message.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}/messages/{messageId}/{channel}/variants/{variantId}
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            messageId : REQUIRED : The message ID.
            channel : REQUIRED : The channel (e.g. "email", "sms", "push").
            variantId : REQUIRED : The variant ID.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if messageId is None:
            raise ValueError("A message ID is required.")
        if channel is None:
            raise ValueError("A channel is required.")
        if variantId is None:
            raise ValueError("A variant ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getCampaignMessageVariant for campaign: {campaignId}"
            )
        path = f"/service/campaigns/{campaignId}/messages/{messageId}/{channel}/variants/{variantId}"
        return self.connector.getData(self.endpoint + path)

    def getCampaignPublishingNotifications(
        self,
        campaignId: str,
        count: int = None,
        page: int = None,
        orderby: str = None,
        property: str = None,
    ) -> dict:
        """
        Retrieve publishing validation notifications for a campaign.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}/publish/validation
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            count : OPTIONAL : Number of results per page (default 50).
            page : OPTIONAL : Page number for pagination.
            orderby : OPTIONAL : Sort field (default "type").
            property : OPTIONAL : FIQL filter expression.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getCampaignPublishingNotifications for: {campaignId}"
            )
        path = f"/service/campaigns/{campaignId}/publish/validation"
        params = {}
        if count is not None:
            params["count"] = count
        if page is not None:
            params["page"] = page
        if orderby is not None:
            params["orderby"] = orderby
        if property is not None:
            params["property"] = property
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getCampaignPackage(self, campaignId: str, packageId: str) -> dict:
        """
        Retrieve a campaign package by ID.
        Implements GET /journey/campaigns/service/campaigns/{campaignId}/packages/{packageId}
        Arguments:
            campaignId : REQUIRED : The campaign ID.
            packageId : REQUIRED : The package ID.
        """
        if campaignId is None:
            raise ValueError("A campaign ID is required.")
        if packageId is None:
            raise ValueError("A package ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getCampaignPackage for campaign: {campaignId}, package: {packageId}"
            )
        path = f"/service/campaigns/{campaignId}/packages/{packageId}"
        return self.connector.getData(self.endpoint + path)

    # ------------------------------------------------------------------ #
    # Workflow Resource                                                    #
    # ------------------------------------------------------------------ #

    def getWorkflow(self, workflowId: str) -> dict:
        """
        Retrieve a workflow by ID.
        Implements GET /journey/campaigns/service/workflows/{workflowId}
        Arguments:
            workflowId : REQUIRED : The workflow ID.
        """
        if workflowId is None:
            raise ValueError("A workflow ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getWorkflow with id: {workflowId}")
        path = f"/service/workflows/{workflowId}"
        return self.connector.getData(self.endpoint + path)

    # ------------------------------------------------------------------ #
    # Metadata Resource                                                    #
    # ------------------------------------------------------------------ #

    def getSurfaces(
        self,
        count: int = None,
        page: int = None,
        orderby: str = None,
        channel: str = None,
        property: str = None,
        type: str = None,
    ) -> dict:
        """
        Retrieve channel surfaces (app configurations).
        Implements GET /journey/campaigns/service/metadata/surfaces
        Arguments:
            count : OPTIONAL : Number of results per page (default 50).
            page : OPTIONAL : Page number for pagination.
            orderby : OPTIONAL : Sort field (default "surfaceName").
            channel : OPTIONAL : Filter by channel (default "inapp").
            property : OPTIONAL : FIQL filter expression.
            type : OPTIONAL : One of "appConfigurationId", "channelConfigurationId",
                "surfaceId", "brandingPresetId".
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getSurfaces")
        path = "/service/metadata/surfaces"
        params = {}
        if count is not None:
            params["count"] = count
        if page is not None:
            params["page"] = page
        if orderby is not None:
            params["orderby"] = orderby
        if channel is not None:
            params["channel"] = channel
        if property is not None:
            params["property"] = property
        if type is not None:
            params["type"] = type
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getSurface(self, channel: str, surfaceId: str, type: str = None) -> dict:
        """
        Retrieve a specific channel surface by channel and ID.
        Implements GET /journey/campaigns/service/metadata/surfaces/{channel}/{surfaceId}
        Arguments:
            channel : REQUIRED : The channel name.
            surfaceId : REQUIRED : The surface ID.
            type : OPTIONAL : Surface type filter.
        """
        if channel is None:
            raise ValueError("A channel is required.")
        if surfaceId is None:
            raise ValueError("A surface ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getSurface for channel: {channel}, id: {surfaceId}"
            )
        path = f"/service/metadata/surfaces/{channel}/{surfaceId}"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )
