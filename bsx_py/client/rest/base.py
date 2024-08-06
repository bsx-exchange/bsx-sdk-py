import json
from http import HTTPStatus

import aiohttp
import requests

from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.exception import BSXRequestException, UnknownException, UnauthenticatedException


class RestClient(object):
    domain: str

    def __init__(self, domain: str):
        self.domain = domain

    def post(self, endpoint: str, body: dict = None, headers: dict = None):
        response = requests.post(f"{self.domain}{endpoint}", json=body, headers=self._headers(headers))
        return self._handle_response(response.text, response.status_code)

    def delete(self, endpoint: str, params: dict = None, body: dict = None, headers: dict = None):
        response = requests.delete(f"{self.domain}{endpoint}", params=params, json=body, headers=self._headers(headers))
        return self._handle_response(response.text, response.status_code)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        response = requests.get(f"{self.domain}{endpoint}", params=params, headers=self._headers(headers))
        return self._handle_response(response.text, response.status_code)

    async def post_async(self, endpoint: str, body: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{self.domain}{endpoint}", json=body, headers=self._headers(headers)
            ) as response:
                resp_body = await response.text()
                status_code = response.status
                return self._handle_response(resp_body=resp_body, status_code=status_code)

    async def delete_async(self, endpoint: str, params: dict = None, body: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f"{self.domain}{endpoint}", params=params, json=body, headers=self._headers(headers)
            ) as response:
                resp_body = await response.text()
                status_code = response.status
                return self._handle_response(resp_body=resp_body, status_code=status_code)

    async def get_async(self, endpoint: str, params: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{self.domain}{endpoint}", params=params, headers=self._headers(headers)
            ) as response:
                resp_body = await response.text()
                status_code = response.status
                return self._handle_response(resp_body=resp_body, status_code=status_code)

    def _headers(self, headers: dict) -> dict:
        if headers is None:
            headers = {}

        headers["accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        return headers

    def _handle_response(self, resp_body: str, status_code: int):
        if status_code != HTTPStatus.OK.value:
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

    def _headers(self, headers: dict) -> dict:
        headers = super()._headers(headers)
        if headers is None:
            headers = {}

        api_key = self._acc_info.get_api_key()
        headers['bsx-key'] = api_key.api_key
        headers['bsx-secret'] = api_key.api_secret

        return headers

