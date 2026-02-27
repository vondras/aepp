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
from typing import Union
from .configs import ConnectObject

_AJO_ORCHESTRATION_PATH = "/journey/orchestration"


class CustomActionManager:
    """
    Client for the AJO capping and throttling configuration APIs.

    These APIs govern how Journey Optimizer rate-limits outbound calls made by
    custom actions and data sources.  Configurations are created per endpoint
    URL (capping) or per organisation (throttling).

    Source spec: ``static/journeys-throttling.yaml``
    (AdobeDocs/journey-optimizer-apis)

    Base URL: ``{ajo_base_url}/journey/orchestration``

    Notes:
        - Only **one** throttling configuration is allowed per organisation.
        - Throttling configurations must be created against a production sandbox.
        - Capping configurations can be deployed/undeployed independently.

    Required IMS scopes:
        - ``journey_optimizer_manage`` (or equivalent orchestration scope)

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
            _base = _override.rstrip("/")
        else:
            _base = self.connector.endpoints.get("global", "https://platform.adobe.io")
        self.orchestrationBaseUrl = f"{_base}{_AJO_ORCHESTRATION_PATH}"

    # ------------------------------------------------------------------
    # Capping configurations  (endpointConfigs)
    # ------------------------------------------------------------------

    def get_capping_configs(self) -> list:
        """
        List all capping configurations for the current sandbox.

        Implements ``GET /journey/orchestration/endpointConfigs``.

        Returns:
            list of capping configuration dicts.
        """
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs"
        res = self.connector.getData(endpoint)
        if isinstance(res, dict):
            return res.get("items", res.get("requestList", [res]))
        return res

    def create_capping_config(self, config_def: dict) -> dict:
        """
        Create a capping configuration.

        Implements ``POST /journey/orchestration/endpointConfigs``.

        Required fields in ``config_def``: ``url``, ``methods``, ``services``,
        ``orgId``.

        Arguments:
            config_def : REQUIRED : Capping configuration dict.

        Returns:
            dict of the created configuration (includes ``uid``).
        """
        if not config_def:
            raise ValueError("config_def is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs"
        return self.connector.postData(endpoint, data=config_def)

    def get_capping_config(self, uid: str) -> dict:
        """
        Fetch a capping configuration by UID.

        Implements ``GET /journey/orchestration/endpointConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.

        Returns:
            dict representing the capping configuration.
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/{uid}"
        return self.connector.getData(endpoint)

    def update_capping_config(self, uid: str, config_def: dict) -> dict:
        """
        Update a capping configuration.

        Implements ``PUT /journey/orchestration/endpointConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.
            config_def : REQUIRED : Updated configuration dict.

        Returns:
            dict of the updated configuration.
        """
        if not uid:
            raise ValueError("uid is required")
        if not config_def:
            raise ValueError("config_def is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/{uid}"
        return self.connector.putData(endpoint, data=config_def)

    def delete_capping_config(self, uid: str) -> int:
        """
        Delete a capping configuration.

        Implements ``DELETE /journey/orchestration/endpointConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.

        Returns:
            HTTP status code (200 on success).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/{uid}"
        return self.connector.deleteData(endpoint)

    def can_deploy_capping_config(self, uid: str) -> dict:
        """
        Check whether a capping configuration can be deployed.

        Implements ``GET /journey/orchestration/endpointConfigs/canDeploy/{uid}``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.

        Returns:
            dict with ``canDeploy`` bool and optional ``errors`` / ``warnings``.
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/canDeploy/{uid}"
        return self.connector.getData(endpoint)

    def deploy_capping_config(self, uid: str) -> dict:
        """
        Deploy a capping configuration.

        Implements ``POST /journey/orchestration/endpointConfigs/{uid}/deploy``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.

        Returns:
            dict (empty body on success; HTTP 200).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/{uid}/deploy"
        return self.connector.postData(endpoint)

    def undeploy_capping_config(self, uid: str) -> dict:
        """
        Undeploy a capping configuration.

        Implements ``POST /journey/orchestration/endpointConfigs/{uid}/undeploy``.

        Arguments:
            uid : REQUIRED : Capping configuration unique ID.

        Returns:
            dict (empty body on success; HTTP 200).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/endpointConfigs/{uid}/undeploy"
        return self.connector.postData(endpoint)

    # ------------------------------------------------------------------
    # Throttling configurations  (throttlingConfigs)
    # ------------------------------------------------------------------

    def get_throttling_configs(self) -> list:
        """
        List all throttling configurations for the current organisation.

        Implements ``GET /journey/orchestration/throttlingConfigs``.

        Returns:
            list of throttling configuration dicts.
        """
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs"
        res = self.connector.getData(endpoint)
        if isinstance(res, dict):
            return res.get("items", res.get("requestList", [res]))
        return res

    def create_throttling_config(self, config_def: dict) -> dict:
        """
        Create a throttling configuration.

        Implements ``POST /journey/orchestration/throttlingConfigs``.

        Only one throttling configuration is allowed per organisation and it
        must be created against a production sandbox.  Required fields:
        ``maxThroughput``, ``urlPattern``, ``methods``.

        Arguments:
            config_def : REQUIRED : Throttling configuration dict.

        Returns:
            dict of the created configuration (includes ``uid``).
        """
        if not config_def:
            raise ValueError("config_def is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs"
        return self.connector.postData(endpoint, data=config_def)

    def get_throttling_config(self, uid: str) -> dict:
        """
        Fetch a throttling configuration by UID.

        Implements ``GET /journey/orchestration/throttlingConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Throttling configuration unique ID.

        Returns:
            dict representing the throttling configuration.
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs/{uid}"
        return self.connector.getData(endpoint)

    def update_throttling_config(self, uid: str, config_def: dict) -> dict:
        """
        Update a throttling configuration.

        Implements ``PUT /journey/orchestration/throttlingConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Throttling configuration unique ID.
            config_def : REQUIRED : Updated configuration dict.

        Returns:
            dict of the updated configuration.
        """
        if not uid:
            raise ValueError("uid is required")
        if not config_def:
            raise ValueError("config_def is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs/{uid}"
        return self.connector.putData(endpoint, data=config_def)

    def delete_throttling_config(self, uid: str) -> int:
        """
        Delete a throttling configuration.

        Implements ``DELETE /journey/orchestration/throttlingConfigs/{uid}``.

        Arguments:
            uid : REQUIRED : Throttling configuration unique ID.

        Returns:
            HTTP status code (204 on success).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs/{uid}"
        return self.connector.deleteData(endpoint)

    def deploy_throttling_config(self, uid: str) -> dict:
        """
        Deploy a throttling configuration.

        Implements ``POST /journey/orchestration/throttlingConfigs/{uid}/deploy``.

        Arguments:
            uid : REQUIRED : Throttling configuration unique ID.

        Returns:
            dict (empty body on success; HTTP 204).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs/{uid}/deploy"
        return self.connector.postData(endpoint)

    def undeploy_throttling_config(self, uid: str) -> dict:
        """
        Undeploy a throttling configuration.

        Implements ``POST /journey/orchestration/throttlingConfigs/{uid}/undeploy``.

        Arguments:
            uid : REQUIRED : Throttling configuration unique ID.

        Returns:
            dict (empty body on success; HTTP 204).
        """
        if not uid:
            raise ValueError("uid is required")
        endpoint = f"{self.orchestrationBaseUrl}/throttlingConfigs/{uid}/undeploy"
        return self.connector.postData(endpoint)
