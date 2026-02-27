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


class Suppression(_AJOBase):
    """
    Class to manage Adobe Journey Optimizer suppression and allow lists.
    Implements the suppression.yaml OpenAPI spec.
    Documentation: https://experienceleague.adobe.com/en/docs/journey-optimizer/using/channel-configuration/manage-suppression-list
    """

    def __init__(
        self,
        config: Union[dict, ConnectObject] = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,
    ):
        """
        Instantiate the Suppression class.
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
    # Addresses                                                            #
    # ------------------------------------------------------------------ #

    def listAddresses(
        self,
        type: str = None,
        orderby: str = None,
        limit: int = None,
        start: str = None,
        property: str = None,
    ) -> dict:
        """
        Query suppressed or allowed email addresses.
        Implements GET /ajo/config/suppression/addresses
        Arguments:
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
            orderby : OPTIONAL : Sort field (default "-creationdate").
            limit : OPTIONAL : Maximum number of results (default 20).
            start : OPTIONAL : Pagination cursor.
            property : OPTIONAL : FIQL filter expression.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listAddresses")
        path = "/config/suppression/addresses"
        params = {}
        if type is not None:
            params["type"] = type
        if orderby is not None:
            params["orderby"] = orderby
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def addAddresses(self, data: list, type: str = None) -> list:
        """
        Add one or more suppressed or allowed email addresses.
        Implements POST /ajo/config/suppression/addresses
        Arguments:
            data : REQUIRED : List of address objects to add.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if data is None:
            raise ValueError("An address list is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting addAddresses")
        path = "/config/suppression/addresses"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.postData(
            self.endpoint + path,
            data=data,
            params=params if params else None,
        )

    def getAddress(self, email: str, type: str = None) -> dict:
        """
        Query a specific suppressed or allowed email address.
        Implements GET /ajo/config/suppression/addresses/{email}
        Arguments:
            email : REQUIRED : The email address to look up.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if email is None:
            raise ValueError("An email address is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getAddress for: {email}")
        path = f"/config/suppression/addresses/{email}"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def deleteAddress(self, email: str, type: str = None) -> Union[int, dict]:
        """
        Delete a specific suppressed or allowed email address.
        Implements DELETE /ajo/config/suppression/addresses/{email}
        Arguments:
            email : REQUIRED : The email address to delete.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if email is None:
            raise ValueError("An email address is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteAddress for: {email}")
        path = f"/config/suppression/addresses/{email}"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.deleteData(
            self.endpoint + path, params=params if params else None
        )

    # ------------------------------------------------------------------ #
    # Domains                                                              #
    # ------------------------------------------------------------------ #

    def listDomains(
        self,
        type: str = None,
        orderby: str = None,
        limit: int = None,
        start: str = None,
        property: str = None,
    ) -> dict:
        """
        Query suppressed or allowed domains.
        Implements GET /ajo/config/suppression/domains
        Arguments:
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
            orderby : OPTIONAL : Sort field (default "-creationdate").
            limit : OPTIONAL : Maximum number of results (default 20).
            start : OPTIONAL : Pagination cursor.
            property : OPTIONAL : FIQL filter expression.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listDomains")
        path = "/config/suppression/domains"
        params = {}
        if type is not None:
            params["type"] = type
        if orderby is not None:
            params["orderby"] = orderby
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def addDomains(self, data: list, type: str = None) -> list:
        """
        Add one or more suppressed or allowed domains.
        Implements POST /ajo/config/suppression/domains
        Arguments:
            data : REQUIRED : List of domain objects to add.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if data is None:
            raise ValueError("A domain list is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting addDomains")
        path = "/config/suppression/domains"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.postData(
            self.endpoint + path,
            data=data,
            params=params if params else None,
        )

    def getDomain(self, domain: str, type: str = None) -> dict:
        """
        Query a specific suppressed or allowed domain.
        Implements GET /ajo/config/suppression/domains/{domain}
        Arguments:
            domain : REQUIRED : The domain to look up.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if domain is None:
            raise ValueError("A domain is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getDomain for: {domain}")
        path = f"/config/suppression/domains/{domain}"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def deleteDomain(self, domain: str, type: str = None) -> Union[int, dict]:
        """
        Delete a specific suppressed or allowed domain.
        Implements DELETE /ajo/config/suppression/domains/{domain}
        Arguments:
            domain : REQUIRED : The domain to delete.
            type : OPTIONAL : "client" for suppressed, "allowed" for allow list.
        """
        if domain is None:
            raise ValueError("A domain is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteDomain for: {domain}")
        path = f"/config/suppression/domains/{domain}"
        params = {}
        if type is not None:
            params["type"] = type
        return self.connector.deleteData(
            self.endpoint + path, params=params if params else None
        )

    # ------------------------------------------------------------------ #
    # Upload Jobs                                                          #
    # ------------------------------------------------------------------ #

    def uploadSuppression(self, file_path: str) -> dict:
        """
        Upload a CSV file of suppressed or allowed entities.
        Implements POST /ajo/config/suppression/uploads
        Arguments:
            file_path : REQUIRED : Path to the CSV file to upload.
        """
        if file_path is None:
            raise ValueError("A file path is required.")
        if self.loggingEnabled:
            self.logger.debug("Starting uploadSuppression")
        path = "/config/suppression/uploads"
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        return self.connector.postData(
            self.endpoint + path, bytesData=file_bytes
        )

    def listUploadJobs(
        self,
        orderby: str = None,
        limit: int = None,
        start: str = None,
        property: str = None,
    ) -> dict:
        """
        Fetch upload jobs for suppressed or allowed entities.
        Implements GET /ajo/config/suppression/uploads
        Arguments:
            orderby : OPTIONAL : Sort field (default "-creationdate").
            limit : OPTIONAL : Maximum number of results (default 20).
            start : OPTIONAL : Pagination cursor.
            property : OPTIONAL : FIQL filter expression.
        """
        if self.loggingEnabled:
            self.logger.debug("Starting listUploadJobs")
        path = "/config/suppression/uploads"
        params = {}
        if orderby is not None:
            params["orderby"] = orderby
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if property is not None:
            params["property"] = property
        return self.connector.getData(
            self.endpoint + path, params=params if params else None
        )

    def getUploadJob(self, jobId: str) -> dict:
        """
        Query a specific upload job.
        Implements GET /ajo/config/suppression/uploads/{jobId}
        Arguments:
            jobId : REQUIRED : The upload job ID.
        """
        if jobId is None:
            raise ValueError("A job ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting getUploadJob for: {jobId}")
        path = f"/config/suppression/uploads/{jobId}"
        return self.connector.getData(self.endpoint + path)

    def deleteUploadJob(self, jobId: str) -> Union[int, dict]:
        """
        Delete a specific upload job record (does not delete the suppressions created by the job).
        Implements DELETE /ajo/config/suppression/uploads/{jobId}
        Arguments:
            jobId : REQUIRED : The upload job ID.
        """
        if jobId is None:
            raise ValueError("A job ID is required.")
        if self.loggingEnabled:
            self.logger.debug(f"Starting deleteUploadJob for: {jobId}")
        path = f"/config/suppression/uploads/{jobId}"
        return self.connector.deleteData(self.endpoint + path)

    def deleteAllSuppressions(
        self, imsOrgId: str, sandboxId: str
    ) -> Union[int, dict]:
        """
        Delete all suppressions for a given IMS Org and Sandbox.
        Implements DELETE /ajo/config/suppression/admin/{imsOrgId}/{sandboxId}
        Arguments:
            imsOrgId : REQUIRED : IMS Organization ID.
            sandboxId : REQUIRED : Sandbox ID.
        """
        if imsOrgId is None:
            raise ValueError("An IMS Org ID is required.")
        if sandboxId is None:
            raise ValueError("A Sandbox ID is required.")
        if self.loggingEnabled:
            self.logger.debug(
                f"Starting deleteAllSuppressions for org: {imsOrgId}, sandbox: {sandboxId}"
            )
        path = f"/config/suppression/admin/{imsOrgId}/{sandboxId}"
        return self.connector.deleteData(self.endpoint + path)
