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


class Messaging(_AJOBase):
    """
    Class to trigger Adobe Journey Optimizer campaigns using the Interactive Message
    Execution API.
    Implements the messaging.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/docs/journey-optimizer/using/campaigns/create-campaign.html
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Messaging class.
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
    # Executions                                                           #
    # ------------------------------------------------------------------ #

    def triggerUnitaryExecution(self, data: dict) -> dict:
        """
        Trigger a unitary (single-profile) message execution.
        Implements POST /ajo/im/executions/unitary
        Arguments:
            data : REQUIRED : Execution request payload (campaignId, recipient, etc.).
        """
        if data is None:
            raise ValueError("An execution request payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting triggerUnitaryExecution")
        path = "/im/executions/unitary"
        return self.connector.postData(self.endpoint + path, data=data)

    def triggerAudienceExecution(self, data: dict) -> dict:
        """
        Trigger or schedule an audience-based message execution.
        Implements POST /ajo/im/executions/audience
        Arguments:
            data : REQUIRED : Execution request payload (campaignId, audience, etc.).
        """
        if data is None:
            raise ValueError("An execution request payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting triggerAudienceExecution")
        path = "/im/executions/audience"
        return self.connector.postData(self.endpoint + path, data=data)

    def getAudienceExecutionStatus(self, executionId: str) -> dict:
        """
        Get the execution status for an audience-based message execution.
        Implements GET /ajo/im/executions/audience/{executionId}
        Arguments:
            executionId : REQUIRED : The execution ID.
        """
        if executionId is None:
            raise ValueError("An execution ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getAudienceExecutionStatus for: {executionId}"
            )
        path = f"/im/executions/audience/{executionId}"
        return self.connector.getData(self.endpoint + path)

    def getScheduledExecutionStatus(self, scheduleId: str) -> dict:
        """
        Get the execution status for a scheduled audience-based message execution.
        Implements GET /ajo/im/executions/schedules/{scheduleId}
        Arguments:
            scheduleId : REQUIRED : The schedule ID.
        """
        if scheduleId is None:
            raise ValueError("A schedule ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting getScheduledExecutionStatus for: {scheduleId}"
            )
        path = f"/im/executions/schedules/{scheduleId}"
        return self.connector.getData(self.endpoint + path)

    def deleteScheduledExecution(self, scheduleId: str) -> Union[int, dict]:
        """
        Delete a scheduled campaign execution before it is triggered.
        Implements DELETE /ajo/im/executions/schedules/{scheduleId}
        Arguments:
            scheduleId : REQUIRED : The schedule ID.
        """
        if scheduleId is None:
            raise ValueError("A schedule ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting deleteScheduledExecution for: {scheduleId}"
            )
        path = f"/im/executions/schedules/{scheduleId}"
        return self.connector.deleteData(self.endpoint + path)

    def triggerHighThroughputExecution(self, data: dict) -> dict:
        """
        Trigger a high-throughput unitary message execution.
        Implements POST /ajo/im/executions/highthroughput
        Arguments:
            data : REQUIRED : Execution request payload.
        """
        if data is None:
            raise ValueError("An execution request payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting triggerHighThroughputExecution")
        path = "/im/executions/highthroughput"
        return self.connector.postData(self.endpoint + path, data=data)

    def getHealth(self) -> dict:
        """
        Get the health status of the Interactive Message Execution service.
        Implements GET /ajo/im/health
        """
        if self.loggingEnabled:
            self.logger.debug("Starting getHealth")
        path = "/im/health"
        return self.connector.getData(self.endpoint + path)
