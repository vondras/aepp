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
from copy import deepcopy

# Vendor media types defined by the content.yaml OpenAPI spec
_TEMPLATE_CONTENT_TYPE = "application/vnd.adobe.ajo.template.v1+json"
_TEMPLATE_LIST_ACCEPT = "application/vnd.adobe.ajo.template-list.v1+json"
_FRAGMENT_CONTENT_TYPE = "application/vnd.adobe.ajo.fragment.v1+json"
_FRAGMENT_LIST_ACCEPT = "application/vnd.adobe.ajo.fragment-list.v1+json"


class Content(_AJOBase):
    """
    Class to manage Adobe Journey Optimizer Content Templates and Fragments.
    Implements the content.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/en/docs/journey-optimizer/using/content-management/content-templates/content-templates
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Content class.
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
            + aepp.config.endpoints["ajo_content"]
        )


    # ------------------------------------------------------------------ #
    # Content Templates                                                    #
    # ------------------------------------------------------------------ #

    def createTemplate(self, data: dict) -> dict:
        """
        Create a new content template.
        Implements POST /ajo/content/templates
        Arguments:
            data : REQUIRED : Content template payload.
        """
        if data is None:
            raise ValueError("A template payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting createTemplate")
        path = "/templates"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _TEMPLATE_CONTENT_TYPE
        res = self.connector.postData(self.endpoint + path, data=data, headers=headers)
        return res

    def listTemplates(
        self,
        orderBy: str = None,
        limit: int = None,
        start: str = None,
        property: str = None,
    ) -> dict:
        """
        List content templates.
        Implements GET /ajo/content/templates
        Arguments:
            orderBy : OPTIONAL : Sort criteria.
            limit : OPTIONAL : Maximum number of results per page.
            start : OPTIONAL : Pagination cursor.
            property : OPTIONAL : Filtering property expression.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listTemplates")
        path = "/templates"
        params = {}
        if orderBy is not None:
            params["orderBy"] = orderBy
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        headers = deepcopy(self.header)
        headers["Accept"] = _TEMPLATE_LIST_ACCEPT
        res = self.connector.getData(
            self.endpoint + path,
            params=params if params else None,
            headers=headers,
        )
        return res

    def getTemplate(self, templateId: str) -> dict:
        """
        Fetch a content template by ID.
        Implements GET /ajo/content/templates/{templateId}
        Arguments:
            templateId : REQUIRED : The content template ID.
        """
        if templateId is None:
            raise ValueError("A template ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getTemplate with id: {templateId}")
        path = f"/templates/{templateId}"
        headers = deepcopy(self.header)
        headers["Accept"] = _TEMPLATE_CONTENT_TYPE
        res = self.connector.getData(self.endpoint + path, headers=headers)
        return res

    def putTemplate(self, templateId: str, data: dict, if_match: str = None) -> dict:
        """
        Update a content template by ID (full replacement).
        Implements PUT /ajo/content/templates/{templateId}
        Arguments:
            templateId : REQUIRED : The content template ID.
            data : REQUIRED : Updated content template payload.
            if_match : OPTIONAL : ETag value for optimistic concurrency control.
        """
        if templateId is None:
            raise ValueError("A template ID is required.")
        if data is None:
            raise ValueError("A template payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting putTemplate with id: {templateId}")
        path = f"/templates/{templateId}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _TEMPLATE_CONTENT_TYPE
        if if_match is not None:
            headers["If-Match"] = if_match
        res = self.connector.putData(self.endpoint + path, data=data, headers=headers)
        return res

    def deleteTemplate(self, templateId: str) -> Union[int, dict]:
        """
        Delete a content template by ID.
        Implements DELETE /ajo/content/templates/{templateId}
        Arguments:
            templateId : REQUIRED : The content template ID.
        """
        if templateId is None:
            raise ValueError("A template ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteTemplate with id: {templateId}")
        path = f"/templates/{templateId}"
        res = self.connector.deleteData(self.endpoint + path)
        return res

    def patchTemplate(
        self, templateId: str, operations: list, if_match: str = None
    ) -> dict:
        """
        Partially update a content template by ID (JSON Patch).
        Implements PATCH /ajo/content/templates/{templateId}
        Arguments:
            templateId : REQUIRED : The content template ID.
            operations : REQUIRED : List of JSON Patch operation objects.
            if_match : OPTIONAL : ETag value for optimistic concurrency control.
        """
        if templateId is None:
            raise ValueError("A template ID is required.")
        if operations is None:
            raise ValueError("A list of patch operations is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting patchTemplate with id: {templateId}")
        path = f"/templates/{templateId}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = "application/json-patch+json"
        if if_match is not None:
            headers["If-Match"] = if_match
        res = self.connector.patchData(
            self.endpoint + path, data=operations, headers=headers
        )
        return res

    # ------------------------------------------------------------------ #
    # Content Fragments                                                    #
    # ------------------------------------------------------------------ #

    def createFragment(self, data: dict) -> dict:
        """
        Create a new content fragment.
        Implements POST /ajo/content/fragments
        Arguments:
            data : REQUIRED : Content fragment payload.
        """
        if data is None:
            raise ValueError("A fragment payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting createFragment")
        path = "/fragments"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _FRAGMENT_CONTENT_TYPE
        res = self.connector.postData(self.endpoint + path, data=data, headers=headers)
        return res

    def listFragments(
        self,
        orderBy: str = None,
        limit: int = None,
        start: str = None,
        property: str = None,
    ) -> dict:
        """
        List content fragments.
        Implements GET /ajo/content/fragments
        Arguments:
            orderBy : OPTIONAL : Sort criteria.
            limit : OPTIONAL : Maximum number of results per page.
            start : OPTIONAL : Pagination cursor.
            property : OPTIONAL : Filtering property expression.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listFragments")
        path = "/fragments"
        params = {}
        if orderBy is not None:
            params["orderBy"] = orderBy
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        headers = deepcopy(self.header)
        headers["Accept"] = _FRAGMENT_LIST_ACCEPT
        res = self.connector.getData(
            self.endpoint + path,
            params=params if params else None,
            headers=headers,
        )
        return res

    def getFragment(self, fragmentId: str) -> dict:
        """
        Fetch a content fragment by ID.
        Implements GET /ajo/content/fragments/{fragmentId}
        Arguments:
            fragmentId : REQUIRED : The content fragment ID.
        """
        if fragmentId is None:
            raise ValueError("A fragment ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getFragment with id: {fragmentId}")
        path = f"/fragments/{fragmentId}"
        headers = deepcopy(self.header)
        headers["Accept"] = _FRAGMENT_CONTENT_TYPE
        res = self.connector.getData(self.endpoint + path, headers=headers)
        return res

    def putFragment(self, fragmentId: str, data: dict, if_match: str = None) -> dict:
        """
        Update a content fragment by ID (full replacement).
        Implements PUT /ajo/content/fragments/{fragmentId}
        Arguments:
            fragmentId : REQUIRED : The content fragment ID.
            data : REQUIRED : Updated content fragment payload.
            if_match : OPTIONAL : ETag value for optimistic concurrency control.
        """
        if fragmentId is None:
            raise ValueError("A fragment ID is required.")
        if data is None:
            raise ValueError("A fragment payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting putFragment with id: {fragmentId}")
        path = f"/fragments/{fragmentId}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _FRAGMENT_CONTENT_TYPE
        if if_match is not None:
            headers["If-Match"] = if_match
        res = self.connector.putData(self.endpoint + path, data=data, headers=headers)
        return res

    def patchFragment(
        self, fragmentId: str, operations: list, if_match: str = None
    ) -> dict:
        """
        Partially update a content fragment by ID (JSON Patch).
        Implements PATCH /ajo/content/fragments/{fragmentId}
        Arguments:
            fragmentId : REQUIRED : The content fragment ID.
            operations : REQUIRED : List of JSON Patch operation objects.
            if_match : OPTIONAL : ETag value for optimistic concurrency control.
        """
        if fragmentId is None:
            raise ValueError("A fragment ID is required.")
        if operations is None:
            raise ValueError("A list of patch operations is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting patchFragment with id: {fragmentId}")
        path = f"/fragments/{fragmentId}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = "application/json-patch+json"
        if if_match is not None:
            headers["If-Match"] = if_match
        res = self.connector.patchData(
            self.endpoint + path, data=operations, headers=headers
        )
        return res

    def publishFragment(self, data: dict) -> dict:
        """
        Publish a content fragment.
        Implements POST /ajo/content/fragments/publications
        Arguments:
            data : REQUIRED : Publication payload.
        """
        if data is None:
            raise ValueError("A publication payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting publishFragment")
        path = "/fragments/publications"
        res = self.connector.postData(self.endpoint + path, data=data)
        return res

    def getLiveFragment(self, fragmentId: str) -> dict:
        """
        Retrieve the live (published) version of a fragment.
        Implements GET /ajo/content/fragments/{fragmentId}/live
        Arguments:
            fragmentId : REQUIRED : The content fragment ID.
        """
        if fragmentId is None:
            raise ValueError("A fragment ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getLiveFragment with id: {fragmentId}")
        path = f"/fragments/{fragmentId}/live"
        headers = deepcopy(self.header)
        headers["Accept"] = _FRAGMENT_CONTENT_TYPE
        res = self.connector.getData(self.endpoint + path, headers=headers)
        return res

    def getLastPublicationStatus(self, fragmentId: str) -> dict:
        """
        Retrieve the last publication status of a fragment.
        Implements GET /ajo/content/fragments/{fragmentId}/publications/latest
        Arguments:
            fragmentId : REQUIRED : The content fragment ID.
        """
        if fragmentId is None:
            raise ValueError("A fragment ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getLastPublicationStatus with id: {fragmentId}"
            )
        path = f"/fragments/{fragmentId}/publications/latest"
        res = self.connector.getData(self.endpoint + path)
        return res
