import os
import json
import simplejson
import xmltodict
import urllib3
import requests

urllib3.disable_warnings() # Disable `Insecure Request` warnings

from ranger_cli.utils import exception_response, status_response, pretty_response


# HTTP status codes
HTTP_STATUS_OK                  = 200
HTTP_STATUS_CREATED             = 201
HTTP_STATUS_NO_CONTENT          = 204

# Base URI
URI_BASE                        = "service/public/v2/api"

# Policy URIs
URI_POLICY                      = URI_BASE + "/policy"
URI_POLICY_ID                   = URI_BASE + "/policy/{policy_id}"
URI_POLICY_BY_ID                = URI_POLICY + "?policyId={policy_id}"
URI_POLICY_BY_NAME              = URI_POLICY + "?policyName={policy_name}"

# Service URIs
URI_SERVICE                     = URI_BASE + "/service"
URI_SERVICE_ID                  = URI_BASE + "/service/{service_id}"
URI_SERVICE_BY_ID               = URI_SERVICE + "?serviceId={service_id}"
URI_SERVICE_BY_NAME             = URI_SERVICE + "?serviceName={service_name}"
URI_SERVICE_POLICIES            = URI_SERVICE + "/{service_name}/policy"
URI_SERVICE_POLICIES_BY_NAME    = URI_SERVICE + "/{service_name}/policy/{policy_name}"

# Plugin URIs
URI_PLUGINS                     = URI_BASE + "/plugins"
URI_PLUGINS_INFO                = URI_PLUGINS + "/info"

# ServiceDef URIs
URI_SERVICEDEF                  = URI_BASE + "/servicedef"
URI_SERVICEDEF_BY_TYPE          = URI_SERVICEDEF + "?serviceType={service_type}"


class RangerClient:

    def __init__(self, endpoint: str, authentication: tuple, verification: str):
        self._endpoint = endpoint
        self._authentication = authentication
        self._verification = verification

    def submit_request(self, method: str, endpoint_path: str, query_params: dict = {}, request_data: dict = {}):

        session = requests.Session()
        session.auth = self._authentication
        session.verify = self._verification
        session.headers = {"Content-type": "application/json"}
        session.allow_redirects = False

        path = os.path.join(self._endpoint, endpoint_path.format(**query_params) if query_params else endpoint_path)

        try:
            if method == "GET":
                response = session.get(path)
            if method == "POST":
                response = session.post(path, data=json.dumps(request_data))
            if method == "PUT":
                response = session.put(path, data=json.dumps(request_data))
            if method == "DELETE":
                response = session.delete(path)

            response.raise_for_status() # Raise exception for all error codes (4xx or 5xx)

        except (requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.RequestException
        ) as exception:

            # In the event that a client or server error is recieved,
            # HTTP status codes 4xx or 5xx, a JSON object with the 
            # exception is returned.

            return exception_response(exception, response)

        else:

            if response.status_code != self.get_status_code(method):
                # Received an 'unexpected' HTTP status code, return status code with reason.
                return status_response(response)

            if response.status_code == HTTP_STATUS_NO_CONTENT:
                # No content returned (HTTP status code 204)
                return True

            try:
                return pretty_response(response.json())
            except simplejson.errors.JSONDecodeError:
                return pretty_response(xmltodict.parse(response.text))
            except Exception as exception:
                return exception_response(exception, response)

    def get_status_code(self, method: str) -> str:
        """
        Returns HTTP status code based on method.

        Args:
            method: HTTP method type
        """
        return getattr(self, method.lower())()

    def get(self):
        """
        Returns `GET` method status code.
        """
        return HTTP_STATUS_OK

    def post(self):
        """
        Returns `POST` method status code.
        """
        return HTTP_STATUS_OK

    def put(self):
        """
        Returns `PUT` method status code.
        """
        return HTTP_STATUS_OK

    def delete(self):
        """
        Returns `DELETE` method status code.
        """
        return HTTP_STATUS_NO_CONTENT


    # Policy APIs
    def get_policy_by_id(self, policy_id: int) -> str:
        """
        Searches for Apache Ranger resource-based policy by id.

        Args:
            policy_id:      Policy ID to be searched.
        """
        return self.submit_request("GET", URI_POLICY_BY_ID, query_params={"policy_id": policy_id})

    def get_policy_by_name(self, policy_name: str) -> str:
        """
        Searches for Apache Ranger resource-based policy by name.

        Args:
            policy_name:    Policy name to be searched.
        """
        return self.submit_request("GET", URI_POLICY_BY_NAME, query_params={"policy_name": policy_name})

    def get_policies(self):
        """
        Returns all Apache Ranger resource-based policy (or policies)
        """
        return self.submit_request("GET", URI_POLICY)

    def get_service_policies(self, service_name: str):
        """
        Searches for Apache Ranger resource-based policy (or policies) by service repository name.

        Args:
            service_name:   Service repository name to be searched.
        """
        return self.submit_request("GET", URI_SERVICE_POLICIES, query_params={"service_name": service_name})

    def create_policy(self, request_data: dict):
        """
        Creates a new Apache Ranger resource-based policy.

        Args:
            request_data:   Configuration properties for resource-based policy
        """
        return self.submit_request("POST", URI_POLICY, request_data=request_data)

    def update_policy(self, policy_id: int, request_data: dict):
        """
        Updates an existing Apache Ranger resource-based policy.

        Args:
            policy_id:      ID for the resource-based policy being updated.
            request_data:   Configuration properties for resource-based policy
        """
        return self.submit_request("PUT", URI_POLICY_ID, query_params={"policy_id": policy_id}, request_data=request_data)

    def delete_policy(self, policy_id: int):
        """
        Deletes an existing Apache Ranger resource-based policy.

        Args:
            policy_id:      ID for the resource-based policy being updated.
        """
        return self.submit_request("DELETE", URI_POLICY_ID, query_params={"policy_id": policy_id})


    # Service APIs
    def get_services(self):
        """
        Returns all Apache Ranger service repository (or repositories).
        """
        return self.submit_request("GET", URI_SERVICE)

    def get_service_by_id(self, service_id: int):
        """
        Searches Apache Ranger service repositories by ID.

        Args:
            service_id:     Service repository ID to be searched.
        """
        return self.submit_request("GET", URI_SERVICE_BY_ID, query_params={"service_id":service_id})

    def get_service_by_name(self, service_name: str):
        """
        Searches Apache Ranger service repositories by name.

        Args:
            service_name:   Service repository name to be searched.
        """
        return self.submit_request("GET", URI_SERVICE_BY_NAME, query_params={"service_name": service_name})

    def create_service(self, request_data: dict):
        """
        Creates a new Apache Ranger service repository.

        Args:
            request_data:   Configuration properties for resource-based policy
        """
        return self.submit_request("POST", URI_SERVICE, request_data=request_data)

    def update_service(self, service_id: int, request_data: dict):
        """
        Updates an existing Apache Ranger service repository.

        Args:
            service_id:     ID for the service repository being updated.
            request_data:   Configuration properties for resource-based policy
        """
        return self.submit_request("PUT", URI_SERVICE_ID, query_params={"service_id": service_id}, request_data=request_data)

    def delete_service(self, service_id: int):
        """
        Deletes an existing Apache Ranger service repository.

        Args:
            service_id:      ID for the service repository being updated.
        """
        return self.submit_request("DELETE", URI_SERVICE_ID, query_params={"service_id": service_id})


    # ServiceDef APIs
    def get_servicedefs(self):
        """
        Returns all Apache Ranger service definitions.
        """
        return self.submit_request("GET", URI_SERVICEDEF)

    def get_servicedefs_by_type(self, service_type: str):
        """
        Returns Apache Ranger service definitions by type.
        """
        return self.submit_request("GET", URI_SERVICEDEF_BY_TYPE, query_params={"service_type": service_type})


    # PluginsInfo APIs
    def get_plugins_info(self):
        """
        Returns all Apache Ranger plugins information.
        """
        return self.submit_request("GET", URI_PLUGINS_INFO)