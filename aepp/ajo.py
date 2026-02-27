#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

# Internal Library
import aepp
from aepp import connector
from copy import deepcopy
from typing import Optional, Union
import logging
from .configs import ConnectObject

# AJO Journey endpoint base path (relative to the platform base URL)
_AJO_JOURNEY_PATH = "/ajo/journey"


class JourneyOptimizer:
    """
    Client for the Adobe Journey Optimizer (AJO) API.

    Implements the Journey retrieval endpoints documented in the
    AdobeDocs journey-optimizer-apis repository (static/journey-retrieve.yaml).
    The base URL defaults to the same platform endpoint as other AEP services
    (https://platform.adobe.io in production) and can be overridden via the
    ``ajo_base_url`` key in the config object or the ``ajo_base_url`` parameter
    of ``aepp.configure``.

    Required IMS scopes (add to your Adobe Developer Console project):
        - ``journey_optimizer_manage`` (or equivalent as shown in your product profile)
        - ``openid``, ``session`` are typically included automatically

    Arguments:
        config : OPTIONAL : ConnectObject or dict with keys matching aepp.config.config_object.
        header : OPTIONAL : header dict (DO NOT MODIFY unless you know what you are doing).
        loggingObject : OPTIONAL : dict with logging configuration keys
                        (level, stream, format, filename, file).
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
            else:
                formatter = logging.Formatter(
                    "%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s::%(lineno)d"
                )
            if loggingObject.get("file"):
                fileHandler = logging.FileHandler(loggingObject["filename"])
                fileHandler.setFormatter(formatter)
                self.logger.addHandler(fileHandler)
            if loggingObject.get("stream"):
                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(formatter)
                self.logger.addHandler(streamHandler)

        if type(config) == ConnectObject:
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

        # Determine the AJO base URL.  Falls back to the AEP global endpoint.
        _config_ajo_base = self.connector.config.get("ajo_base_url") or None
        if _config_ajo_base:
            self.ajoBaseUrl = _config_ajo_base.rstrip("/")
        else:
            self.ajoBaseUrl = self.connector.endpoints.get("global", "https://platform.adobe.io")

    def list_journeys(
        self,
        page: int = 0,
        page_size: int = 100,
        filter: Optional[str] = None,
        fields: Optional[str] = None,
        sort: Optional[str] = None,
        n_results: Optional[int] = None,
    ) -> dict:
        """
        Return a list of journeys from AJO.

        Implements ``GET /ajo/journey`` as defined in
        ``static/journey-retrieve.yaml`` in the AdobeDocs journey-optimizer-apis
        repository.

        Arguments:
            page : OPTIONAL : Page number (0-based). Default 0.
            page_size : OPTIONAL : Number of items per page (1-100). Default 100.
            filter : OPTIONAL : URL-encoded filter string, e.g. ``status=draft``.
            fields : OPTIONAL : Comma-separated list of fields to return, e.g. ``name,status``.
            sort : OPTIONAL : Sort criteria, e.g. ``name=asc``.
            n_results : OPTIONAL : If provided, fetch additional pages automatically
                        until at least ``n_results`` journey records have been collected
                        or all pages are exhausted.  Returns accumulated results dict
                        with the ``results`` key containing all collected journeys.

        Returns:
            dict with keys ``results`` (list), ``page``, ``limit``, ``pages``.
        """
        endpoint = f"{self.ajoBaseUrl}{_AJO_JOURNEY_PATH}"
        params = {"page": page, "pageSize": page_size}
        if filter is not None:
            params["filter"] = filter
        if fields is not None:
            params["fields"] = fields
        if sort is not None:
            params["sort"] = sort

        if self.loggingEnabled:
            self.logger.debug(f"list_journeys called with params: {params}")

        res = self.connector.getData(endpoint, params=params)

        if n_results is None:
            return res

        # Auto-paginate when caller requests a specific number of results.
        collected = list(res.get("results", []))
        total_pages = res.get("pages", 1)
        current_page = page

        while len(collected) < n_results and (current_page + 1) < total_pages:
            current_page += 1
            params["page"] = current_page
            next_res = self.connector.getData(endpoint, params=params)
            next_items = next_res.get("results", [])
            if not next_items:
                break
            collected.extend(next_items)

        result = deepcopy(res)
        result["results"] = collected[:n_results] if n_results else collected
        return result

    def get_journey(self, journey_id: str, include: Optional[str] = None) -> dict:
        """
        Return a single journey by its ID.

        Implements ``GET /ajo/journey/{id}`` as defined in
        ``static/journey-retrieve.yaml`` in the AdobeDocs journey-optimizer-apis
        repository.

        Arguments:
            journey_id : REQUIRED : The journey ID.
            include : OPTIONAL : Comma-separated list of additional data to include
                      in the response (e.g. ``campaigns,rulesets``).

        Returns:
            dict representing the journey object.
        """
        if not journey_id:
            raise ValueError("journey_id is required")
        endpoint = f"{self.ajoBaseUrl}{_AJO_JOURNEY_PATH}/{journey_id}"
        params = {}
        if include is not None:
            params["include"] = include

        if self.loggingEnabled:
            self.logger.debug(f"get_journey called for id={journey_id}")

        return self.connector.getData(endpoint, params=params if params else None)

    def get_journey_ids(
        self,
        page: int = 0,
        page_size: int = 100,
        filter: Optional[str] = None,
    ) -> list:
        """
        Return a list of journey IDs from AJO.

        Convenience helper that calls ``list_journeys`` and extracts the ``id`` field
        from each result entry.

        Arguments:
            page : OPTIONAL : Page number (0-based). Default 0.
            page_size : OPTIONAL : Number of items per page (1-100). Default 100.
            filter : OPTIONAL : URL-encoded filter string.

        Returns:
            list of journey ID strings.
        """
        res = self.list_journeys(page=page, page_size=page_size, filter=filter)
        return [j.get("id") for j in res.get("results", []) if j.get("id")]
