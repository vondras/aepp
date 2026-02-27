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


class OrchestratedDataset(_AJOBase):
    """
    Class to manage the Orchestrated Campaign extension on Adobe Experience Platform datasets.
    Implements the orchestrated-campaign-dataset.yaml OpenAPI spec.
    Documentation: https://developer.adobe.com/journey-optimizer-apis/references/orchestrated-campaign-dataset/
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the OrchestratedDataset class.
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
            + aepp.config.endpoints["ajo_relational"]
        )

    def validateDatasetExtension(self, datasetId: str) -> dict:
        """
        Validate whether the Orchestrated Campaign extension can be applied to a dataset.
        Implements GET /ajo/relational/modeler/datasets/{datasetId}/extensions/validation
        Arguments:
            datasetId : REQUIRED : The dataset ID to validate.
        """
        if datasetId is None:
            raise ValueError("A dataset ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting validateDatasetExtension for: {datasetId}"
            )
        path = f"/modeler/datasets/{datasetId}/extensions/validation"
        return self.connector.getData(self.endpoint + path)

    def enableDatasetExtension(self, data: dict) -> list:
        """
        Enable the Orchestrated Campaign extension on a dataset (asynchronous).
        Implements POST /ajo/relational/modeler/datasets/extensions/enablement
        Arguments:
            data : REQUIRED : Enablement request payload (datasetId, etc.).
        """
        if data is None:
            raise ValueError("An enablement request payload is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting enableDatasetExtension")
        path = "/modeler/datasets/extensions/enablement"
        return self.connector.postData(self.endpoint + path, data=data)

    def getDatasetExtensionJob(self, jobId: str) -> dict:
        """
        Get the status of a dataset extension enablement job.
        Implements GET /ajo/relational/modeler/datasets/extensions/enablement/jobs/{jobId}
        Arguments:
            jobId : REQUIRED : The job ID returned by enableDatasetExtension.
        """
        if jobId is None:
            raise ValueError("A job ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getDatasetExtensionJob for: {jobId}")
        path = f"/modeler/datasets/extensions/enablement/jobs/{jobId}"
        return self.connector.getData(self.endpoint + path)
