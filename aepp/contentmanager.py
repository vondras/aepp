#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

import aepp
from aepp import connector
import logging
from copy import deepcopy
from typing import Optional, Union
from .configs import ConnectObject

_AJO_CONTENT_PATH = "/ajo/content"
_MEDIA_TYPE_TEMPLATE = "application/vnd.adobe.ajo.template.v1+json"
_MEDIA_TYPE_FRAGMENT = "application/vnd.adobe.ajo.fragment.v1+json"


class ContentManager:
    """
    Client for the AJO Content Templates and Fragments API.

    Implements the endpoints documented in
    ``static/content.yaml`` (AdobeDocs/journey-optimizer-apis).

    Base URL: ``{ajo_base_url}/ajo/content``

    Pagination (list endpoints):
        The content API uses cursor-based pagination.  The ``_links.next.href``
        field in list responses contains the next page URL; extract the ``start``
        token from it and pass it to the next call.

    Required IMS scopes:
        - ``journey_optimizer_manage`` (or equivalent content-management scope)

    Arguments:
        config : OPTIONAL : ConnectObject or config dict.
        header : OPTIONAL : Override header dict (DO NOT MODIFY).
        loggingObject : OPTIONAL : Logging configuration dict with keys
                        ``level``, ``stream``, ``format``, ``filename``, ``file``.
    """

    loggingEnabled = False
    logger = None

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ) -> None:
        if loggingObject is not None and sorted(
            ["level", "stream", "format", "filename", "file"]
        ) == sorted(list(loggingObject.keys())):
            self.loggingEnabled = True
            self.logger = logging.getLogger(f"{__name__}")
            self.logger.setLevel(loggingObject["level"])
            if type(loggingObject["format"]) == str:
                formatter = logging.Formatter(loggingObject["format"])
            elif type(loggingObject["format"]) == logging.Formatter:
                formatter = loggingObject["format"]
            if loggingObject["file"]:
                fileHandler = logging.FileHandler(loggingObject["filename"])
                fileHandler.setFormatter(formatter)
                self.logger.addHandler(fileHandler)
            if loggingObject["stream"]:
                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(formatter)
                self.logger.addHandler(streamHandler)
        if type(config) == dict:
            config = config
        elif type(config) == ConnectObject:
            header = config.getConfigHeader()
            config = config.getConfigObject()
        self.connector = connector.AdobeRequest(
            config=config,
            header=header,
            loggingEnabled=self.loggingEnabled,
            logger=self.logger,
        )
        self.sandbox = self.connector.config.get("sandbox", "prod")
        self.header = self.connector.header
        _override = self.connector.config.get("ajo_base_url") or None
        if _override:
            self.ajoBaseUrl = _override.rstrip("/")
        else:
            self.ajoBaseUrl = self.connector.endpoints.get("global", "https://platform.adobe.io")

    # ------------------------------------------------------------------
    # Content Templates
    # ------------------------------------------------------------------

    def list_templates(
        self,
        order_by: Optional[str] = None,
        limit: int = 50,
        start: Optional[str] = None,
        property: Optional[str] = None,
    ) -> dict:
        """
        List content templates.

        Implements ``GET /ajo/content/templates``.

        Arguments:
            order_by : OPTIONAL : Sort field and direction, e.g. ``"modifiedAt=desc"``.
            limit : OPTIONAL : Maximum results per page (default 50).
            start : OPTIONAL : Cursor token from a previous response for pagination.
            property : OPTIONAL : Filter expression, e.g. ``"templateType==html"``.

        Returns:
            dict with an ``items`` list and ``_links`` for pagination.
        """
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates"
        params: dict = {"limit": limit}
        if order_by is not None:
            params["orderBy"] = order_by
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        return self.connector.getData(endpoint, params=params)

    def get_template(self, template_id: str) -> dict:
        """
        Fetch a content template by ID.

        Implements ``GET /ajo/content/templates/{templateId}``.

        Arguments:
            template_id : REQUIRED : The content template ID.

        Returns:
            dict representing the content template.
        """
        if not template_id:
            raise ValueError("template_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates/{template_id}"
        headers = deepcopy(self.header)
        headers["Accept"] = _MEDIA_TYPE_TEMPLATE
        return self.connector.getData(endpoint, headers=headers)

    def create_template(self, template_def: dict) -> dict:
        """
        Create a new content template.

        Implements ``POST /ajo/content/templates``.

        Arguments:
            template_def : REQUIRED : Template definition dict.

        Returns:
            dict with the created template (includes ``id``).
        """
        if not template_def:
            raise ValueError("template_def is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _MEDIA_TYPE_TEMPLATE
        return self.connector.postData(endpoint, data=template_def, headers=headers)

    def update_template(
        self,
        template_id: str,
        template_def: dict,
        etag: Optional[str] = None,
    ) -> dict:
        """
        Replace a content template by ID.

        Implements ``PUT /ajo/content/templates/{templateId}``.

        Arguments:
            template_id : REQUIRED : The content template ID.
            template_def : REQUIRED : Updated template definition dict.
            etag : OPTIONAL : ETag value for optimistic concurrency control.

        Returns:
            dict (empty body on success; HTTP 204).
        """
        if not template_id:
            raise ValueError("template_id is required")
        if not template_def:
            raise ValueError("template_def is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates/{template_id}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _MEDIA_TYPE_TEMPLATE
        if etag is not None:
            headers["If-Match"] = etag
        return self.connector.putData(endpoint, data=template_def, headers=headers)

    def delete_template(self, template_id: str) -> int:
        """
        Delete a content template by ID.

        Implements ``DELETE /ajo/content/templates/{templateId}``.

        Arguments:
            template_id : REQUIRED : The content template ID.

        Returns:
            HTTP status code (204 on success).
        """
        if not template_id:
            raise ValueError("template_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates/{template_id}"
        return self.connector.deleteData(endpoint)

    def validate_template(self, template_id: str) -> dict:
        """
        Validate a content template.

        Implements ``POST /ajo/content/templates/{templateId}/validate``.

        Arguments:
            template_id : REQUIRED : The content template ID.

        Returns:
            dict with validation results.
        """
        if not template_id:
            raise ValueError("template_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/templates/{template_id}/validate"
        return self.connector.postData(endpoint)

    # ------------------------------------------------------------------
    # Content Fragments
    # ------------------------------------------------------------------

    def list_fragments(
        self,
        order_by: Optional[str] = None,
        limit: int = 50,
        start: Optional[str] = None,
        property: Optional[str] = None,
    ) -> dict:
        """
        List content fragments.

        Implements ``GET /ajo/content/fragments``.

        Arguments:
            order_by : OPTIONAL : Sort field and direction, e.g. ``"modifiedAt=desc"``.
            limit : OPTIONAL : Maximum results per page (default 50).
            start : OPTIONAL : Cursor token from a previous response for pagination.
            property : OPTIONAL : Filter expression.

        Returns:
            dict with an ``items`` list and ``_links`` for pagination.
        """
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments"
        params: dict = {"limit": limit}
        if order_by is not None:
            params["orderBy"] = order_by
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        return self.connector.getData(endpoint, params=params)

    def get_fragment(self, fragment_id: str) -> dict:
        """
        Fetch a content fragment by ID.

        Implements ``GET /ajo/content/fragments/{fragmentId}``.

        Arguments:
            fragment_id : REQUIRED : The content fragment ID.

        Returns:
            dict representing the content fragment.
        """
        if not fragment_id:
            raise ValueError("fragment_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments/{fragment_id}"
        headers = deepcopy(self.header)
        headers["Accept"] = _MEDIA_TYPE_FRAGMENT
        return self.connector.getData(endpoint, headers=headers)

    def create_fragment(self, fragment_def: dict) -> dict:
        """
        Create a new content fragment.

        Implements ``POST /ajo/content/fragments``.

        Arguments:
            fragment_def : REQUIRED : Fragment definition dict.

        Returns:
            dict with the created fragment (includes ``id``).
        """
        if not fragment_def:
            raise ValueError("fragment_def is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _MEDIA_TYPE_FRAGMENT
        return self.connector.postData(endpoint, data=fragment_def, headers=headers)

    def update_fragment(
        self,
        fragment_id: str,
        fragment_def: dict,
        etag: Optional[str] = None,
    ) -> dict:
        """
        Replace a content fragment by ID.

        Implements ``PUT /ajo/content/fragments/{fragmentId}``.

        Arguments:
            fragment_id : REQUIRED : The content fragment ID.
            fragment_def : REQUIRED : Updated fragment definition dict.
            etag : OPTIONAL : ETag for optimistic concurrency.

        Returns:
            dict (empty body on success; HTTP 204).
        """
        if not fragment_id:
            raise ValueError("fragment_id is required")
        if not fragment_def:
            raise ValueError("fragment_def is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments/{fragment_id}"
        headers = deepcopy(self.header)
        headers["Content-Type"] = _MEDIA_TYPE_FRAGMENT
        if etag is not None:
            headers["If-Match"] = etag
        return self.connector.putData(endpoint, data=fragment_def, headers=headers)

    def delete_fragment(self, fragment_id: str) -> int:
        """
        Delete a content fragment by ID.

        Implements ``DELETE /ajo/content/fragments/{fragmentId}``.

        Arguments:
            fragment_id : REQUIRED : The content fragment ID.

        Returns:
            HTTP status code (204 on success).
        """
        if not fragment_id:
            raise ValueError("fragment_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments/{fragment_id}"
        return self.connector.deleteData(endpoint)

    def publish_fragment(self, fragment_id: str) -> dict:
        """
        Publish a content fragment.

        Implements ``POST /ajo/content/fragments/{fragmentId}/publish``.

        Arguments:
            fragment_id : REQUIRED : The content fragment ID.

        Returns:
            dict with the published fragment.
        """
        if not fragment_id:
            raise ValueError("fragment_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_CONTENT_PATH}/fragments/{fragment_id}/publish"
        return self.connector.postData(endpoint)
