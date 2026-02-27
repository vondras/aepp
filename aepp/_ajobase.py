#  Copyright 2023 Adobe. All rights reserved.
#  This file is licensed to you under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License. You may obtain a copy
#  of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under
#  the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
#  OF ANY KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.

## Internal modules
import aepp
from aepp import connector

## External modules
import logging
import json
from typing import Union
from .configs import ConnectObject


class _AJOBase:
    """
    Common base class for Adobe Journey Optimizer API modules.

    Centralises:
    - logging handler setup
    - ConnectObject / dict config normalisation
    - AdobeRequest connector creation
    - sandbox header propagation
    - ``__str__`` / ``__repr__``

    Subclasses should call ``super().__init__(...)`` and then set their
    own ``self.endpoint``.
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
        Shared initialisation for all AJO API classes.
        Arguments:
            config : OPTIONAL : config object in the config module. (DO NOT MODIFY)
            header : OPTIONAL : header object in the config module. (DO NOT MODIFY)
            loggingObject : OPTIONAL : logging object to log messages.
        """
        if loggingObject is not None and sorted(
            ["level", "stream", "format", "filename", "file"]
        ) == sorted(list(loggingObject.keys())):
            self.loggingEnabled = True
            self.logger = logging.getLogger(
                f"{type(self).__module__}.{type(self).__name__}"
            )
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
            logger=self.logger,
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

    def __str__(self):
        return json.dumps(
            {
                "class": type(self).__name__,
                "sandbox": self.sandbox,
                "clientId": self.connector.config.get("client_id"),
                "orgId": self.connector.config.get("org_id"),
            },
            indent=2,
        )

    def __repr__(self):
        return json.dumps(
            {
                "class": type(self).__name__,
                "sandbox": self.sandbox,
                "clientId": self.connector.config.get("client_id"),
                "orgId": self.connector.config.get("org_id"),
            },
            indent=2,
        )


def create_ajo_client(
    service: str,
    config: Union[dict, ConnectObject] = aepp.config.config_object,
    header: dict = aepp.config.header,
    loggingObject: dict = None,
    **kwargs,
) -> _AJOBase:
    """
    Factory function that returns an AJO API client for the requested service.

    Arguments:
        service : REQUIRED : One of "journey", "content", or "orchestration".
        config : OPTIONAL : config object in the config module. (DO NOT MODIFY)
        header : OPTIONAL : header object in the config module. (DO NOT MODIFY)
        loggingObject : OPTIONAL : logging object to log messages.

    Returns:
        An instance of Journey, Content, or Orchestration.
    """
    ## Local imports avoid circular-import issues at module load time
    from aepp.journey import Journey
    from aepp.content import Content
    from aepp.orchestration import Orchestration

    _services: dict = {
        "journey": Journey,
        "content": Content,
        "orchestration": Orchestration,
    }
    if not isinstance(service, str):
        raise ValueError(
            f"service must be a string, got {type(service).__name__}"
        )
    cls = _services.get(service.lower())
    if cls is None:
        raise ValueError(
            f"Unknown AJO service '{service}'. Valid values: {list(_services)}"
        )
    return cls(config=config, header=header, loggingObject=loggingObject, **kwargs)
