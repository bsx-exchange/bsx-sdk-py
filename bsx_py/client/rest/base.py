import json
import requests

from http import HTTPStatus

from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.exception import BSXRequestException, UnknownException, UnauthenticatedException


class RestClient(object):
    domain: str

    def __init__(self, domain: str):
        self.domain = domain

    def post(self, endpoint: str, body: dict, headers: dict = None):
        if headers is None:
            headers = {}

        headers["accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        response = requests.post(f"{self.domain}{endpoint}", json=body, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint: str, params: dict, body: dict, headers: dict = None):
        if headers is None:
            headers = {}

        headers["accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        response = requests.delete(f"{self.domain}{endpoint}", params=params, json=body, headers=headers)
        return self._handle_response(response)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        response = requests.get(f"{self.domain}{endpoint}", params=params, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response):
        resp_body = response.text
        if response.status_code != HTTPStatus.OK.value:
            json_body = json.loads(resp_body)
            if "code" in json_body:
                err_code = json_body["code"]
                if err_code == 16:
                    raise UnauthenticatedException()
                else:
                    raise BSXRequestException(
                        err_code, json_body.get("message", "Unknown error"), json_body.get("detail")
                    )
            else:
                raise UnknownException(resp_body)

        return json.loads(resp_body)


class AuthRequiredClient(RestClient):
    def __init__(self, domain: str, acc_info: AccountInfo):
        super().__init__(domain)
        self._acc_info = acc_info

    def post(self, endpoint: str, body: dict, headers: dict = None):
        if headers is None:
            headers = {}

        api_key = self._acc_info.get_api_key()
        print(api_key.api_key)
        headers['bsx-key'] = api_key.api_key
        headers['bsx-secret'] = api_key.api_secret

        return super().post(endpoint, body, headers)

    def delete(self, endpoint: str, params: dict = None, body: dict = None, headers: dict = None):
        if headers is None:
            headers = {}

        api_key = self._acc_info.get_api_key()
        print(api_key.api_key)
        headers['bsx-key'] = api_key.api_key
        headers['bsx-secret'] = api_key.api_secret

        return super().delete(endpoint=endpoint, params=params, body=body, headers=headers)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        if headers is None:
            headers = {}

        api_key = self._acc_info.get_api_key()
        print(api_key.api_key)
        headers['bsx-key'] = api_key.api_key
        headers['bsx-secret'] = api_key.api_secret

        return super().get(endpoint, params, headers)
