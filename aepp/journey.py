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


class Journey(_AJOBase):
    """
    Class to retrieve and manage Adobe Journey Optimizer Journeys.
    Implements the journey-retrieve.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/en/docs/journey-optimizer/using/orchestrate-journeys/about-journeys
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Journey class.
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
    def getJourneys(
        self,
        filter: str = None,
        page: int = None,
        pageSize: int = None,
        fields: str = None,
        sort: str = None,
    ) -> dict:
        """
        Returns a list of journeys based on the provided filters.
        Implements GET /ajo/journey
        Arguments:
            filter : OPTIONAL : URL-encoded search filters (e.g. "status=draft").
            page : OPTIONAL : Page number for pagination (0-based).
            pageSize : OPTIONAL : Number of items per page (1-100).
            fields : OPTIONAL : Comma-separated list of fields to include.
            sort : OPTIONAL : Sort criteria (e.g. "name=asc,metadata.createdAt=desc").
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getJourneys")
        path = "/journey"
        params = {}
        if filter is not None:
            params["filter"] = filter
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if fields is not None:
            params["fields"] = fields
        if sort is not None:
            params["sort"] = sort
        res = self.connector.getData(self.endpoint + path, params=params if params else None)
        return res

    def getJourney(self, journeyId: str, include: str = None) -> dict:
        """
        Returns a journey by its ID.
        Implements GET /ajo/journey/{id}
        Arguments:
            journeyId : REQUIRED : The journey ID.
            include : OPTIONAL : Comma-separated list of additional data to include
                (e.g. "campaigns,rulesets").
        """
        if journeyId is None:
            raise ValueError("A journey ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getJourney with id: {journeyId}")
        path = f"/journey/{journeyId}"
        params = {}
        if include is not None:
            params["include"] = include
        res = self.connector.getData(self.endpoint + path, params=params if params else None)
        return res
