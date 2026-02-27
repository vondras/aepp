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
import logging
from typing import Union
from .configs import ConnectObject
import json


class Orchestration:
    """
    Class to manage Adobe Journey Optimizer capping and throttling configurations.
    Implements the journeys-throttling.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/docs/journey-optimizer/using/configuration/configure-journeys/external-systems/external-systems.html#capping
    """

    ## logging capability
    loggingEnabled = False
    logger = None

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Orchestration class.
        Arguments:
            config : OPTIONAL : config object in the config module. (DO NOT MODIFY)
            header : OPTIONAL : header object in the config module. (DO NOT MODIFY)
            loggingObject : OPTIONAL : logging object to log messages.
        """
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
            pass
        elif type(config) == ConnectObject:
            header = config.getConfigHeader()
            config = config.getConfigObject()
        self.connector = connector.AdobeRequest(
            config=config,
            header=header,
            loggingEnabled=self.loggingEnabled,
            loggingObject=self.logger,
        )
        self.header = self.connector.header
        self.header.update(**kwargs)
        if kwargs.get("sandbox", None) is not None:
            self.sandbox = kwargs.get("sandbox")
            self.connector.config["sandbox"] = kwargs.get("sandbox")
            self.header.update({"x-sandbox-name": kwargs.get("sandbox")})
            self.connector.header.update({"x-sandbox-name": kwargs.get("sandbox")})
        else:
            self.sandbox = self.connector.config["sandbox"]
        self.endpoint = (
            self.connector.config.get("global", aepp.config.endpoints["global"])
            + aepp.config.endpoints["ajo_orchestration"]
        )

    def __str__(self):
        return json.dumps(
            {
                "class": "Orchestration",
                "sandbox": self.sandbox,
                "clientId": self.connector.config.get("client_id"),
                "orgId": self.connector.config.get("org_id"),
            },
            indent=2,
        )

    def __repr__(self):
        return json.dumps(
            {
                "class": "Orchestration",
                "sandbox": self.sandbox,
                "clientId": self.connector.config.get("client_id"),
                "orgId": self.connector.config.get("org_id"),
            },
            indent=2,
        )

    # ------------------------------------------------------------------ #
    # Capping (endpoint) configurations                                   #
    # ------------------------------------------------------------------ #

    def createEndpointConfig(self, data: dict) -> dict:
        """
        Create a capping configuration on a given endpoint.
        Implements POST /journey/orchestration/endpointConfigs
        Arguments:
            data : REQUIRED : Capping configuration payload.
        """
        if data is None:
            raise ValueError("A capping configuration payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting createEndpointConfig")
        path = "/endpointConfigs"
        res = self.connector.postData(self.endpoint + path, data=data)
        return res

    def getEndpointConfig(self, uid: str) -> dict:
        """
        Retrieve a capping configuration by UID.
        Implements GET /journey/orchestration/endpointConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}"
        res = self.connector.getData(self.endpoint + path)
        return res

    def putEndpointConfig(self, uid: str, data: dict) -> dict:
        """
        Update a capping configuration by UID (full replacement).
        Implements PUT /journey/orchestration/endpointConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
            data : REQUIRED : Updated capping configuration payload.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if data is None:
            raise ValueError("A capping configuration payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting putEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}"
        res = self.connector.putData(self.endpoint + path, data=data)
        return res

    def deleteEndpointConfig(self, uid: str) -> dict:
        """
        Delete a capping configuration by UID.
        Implements DELETE /journey/orchestration/endpointConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}"
        res = self.connector.deleteData(self.endpoint + path)
        return res

    def canDeployEndpointConfig(self, uid: str) -> dict:
        """
        Check whether a capping configuration can be deployed.
        Implements GET /journey/orchestration/endpointConfigs/{uid}/canDeploy
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting canDeployEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}/canDeploy"
        res = self.connector.getData(self.endpoint + path)
        return res

    def deployEndpointConfig(self, uid: str) -> dict:
        """
        Deploy a capping configuration.
        Implements POST /journey/orchestration/endpointConfigs/{uid}/deploy
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deployEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}/deploy"
        res = self.connector.postData(self.endpoint + path)
        return res

    def undeployEndpointConfig(self, uid: str) -> dict:
        """
        Undeploy a capping configuration.
        Implements POST /journey/orchestration/endpointConfigs/{uid}/undeploy
        Arguments:
            uid : REQUIRED : Unique ID of the capping configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting undeployEndpointConfig with uid: {uid}")
        path = f"/endpointConfigs/{uid}/undeploy"
        res = self.connector.postData(self.endpoint + path)
        return res

    def listEndpointConfigs(self, data: dict = None) -> dict:
        """
        List capping configurations.
        Implements POST /journey/orchestration/list/endpointConfigs
        Arguments:
            data : OPTIONAL : Filter/pagination payload.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listEndpointConfigs")
        path = "/list/endpointConfigs"
        res = self.connector.postData(self.endpoint + path, data=data)
        return res

    # ------------------------------------------------------------------ #
    # Throttling configurations                                            #
    # ------------------------------------------------------------------ #

    def createThrottlingConfig(self, data: dict) -> dict:
        """
        Create a throttling configuration.
        Implements POST /journey/orchestration/throttlingConfigs
        Arguments:
            data : REQUIRED : Throttling configuration payload (must include
                maxThroughput, urlPattern, and methods).
        """
        if data is None:
            raise ValueError("A throttling configuration payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting createThrottlingConfig")
        path = "/throttlingConfigs"
        res = self.connector.postData(self.endpoint + path, data=data)
        return res

    def getThrottlingConfig(self, uid: str) -> dict:
        """
        Retrieve a throttling configuration by UID.
        Implements GET /journey/orchestration/throttlingConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}"
        res = self.connector.getData(self.endpoint + path)
        return res

    def putThrottlingConfig(self, uid: str, data: dict) -> dict:
        """
        Update a throttling configuration by UID (full replacement).
        Implements PUT /journey/orchestration/throttlingConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
            data : REQUIRED : Updated throttling configuration payload.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if data is None:
            raise ValueError("A throttling configuration payload is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting putThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}"
        res = self.connector.putData(self.endpoint + path, data=data)
        return res

    def deleteThrottlingConfig(self, uid: str) -> dict:
        """
        Delete a throttling configuration by UID.
        Implements DELETE /journey/orchestration/throttlingConfigs/{uid}
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}"
        res = self.connector.deleteData(self.endpoint + path)
        return res

    def canDeployThrottlingConfig(self, uid: str) -> dict:
        """
        Check whether a throttling configuration can be deployed.
        Implements GET /journey/orchestration/throttlingConfigs/{uid}/canDeploy
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting canDeployThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}/canDeploy"
        res = self.connector.getData(self.endpoint + path)
        return res

    def deployThrottlingConfig(self, uid: str) -> dict:
        """
        Deploy a throttling configuration.
        Implements POST /journey/orchestration/throttlingConfigs/{uid}/deploy
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deployThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}/deploy"
        res = self.connector.postData(self.endpoint + path)
        return res

    def undeployThrottlingConfig(self, uid: str) -> dict:
        """
        Undeploy a throttling configuration.
        Implements POST /journey/orchestration/throttlingConfigs/{uid}/undeploy
        Arguments:
            uid : REQUIRED : Unique ID of the throttling configuration.
        """
        if uid is None:
            raise ValueError("A configuration UID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting undeployThrottlingConfig with uid: {uid}")
        path = f"/throttlingConfigs/{uid}/undeploy"
        res = self.connector.postData(self.endpoint + path)
        return res

    def listThrottlingConfigs(self, data: dict = None) -> dict:
        """
        List throttling configurations.
        Implements POST /journey/orchestration/list/throttlingConfigs
        Arguments:
            data : OPTIONAL : Filter/pagination payload.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listThrottlingConfigs")
        path = "/list/throttlingConfigs"
        res = self.connector.postData(self.endpoint + path, data=data)
        return res
