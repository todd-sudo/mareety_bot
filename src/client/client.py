from typing import List, Union, Optional

import requests

from logger import logger as log
from src.client.exeptions import HTTP_EXCEPTIONS


class HttpClient:
    """ HTTP Клиент
    """
    url: str
    headers: dict
    cookies: dict
    json_data: Union[dict, list]
    verify: bool

    def __init__(
            self,
            url: str,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            json_data: Union[dict, list, None] = None,
            verify: bool = False,
    ):
        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}

        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.json_data = json_data
        self.verify = verify

    def _get(self):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            cookies=self.cookies,
            verify=self.verify,
        )
        return response

    def _post_json(self):
        response = requests.post(
            url=self.url,
            headers=self.headers,
            cookies=self.cookies,
            json=self.json_data,
            verify=self.verify,
        )
        return response

    def http_get(self) -> Optional[requests.Response]:
        """ Отправляет GET запрос
        """
        for i in range(10):
            try:
                response = self._get()
                if response:
                    return response
            except HTTP_EXCEPTIONS as err:
                log.error(err)
                continue
            continue

    def http_post_json(self) -> Optional[requests.Response]:
        """ Отправляет POST запрос с JSON
        """
        for i in range(10):
            try:
                response = self._post_json()
                if response:
                    return response
            except HTTP_EXCEPTIONS as err:
                log.error(err)
                continue
            continue
        return None

    @staticmethod
    def decode_json(
            response: requests.Response
    ) -> Union[List[dict], dict, List[list], None]:
        """ Декодирование JSON из ответа
        """
        try:
            data = response.json()
            return data
        except HTTP_EXCEPTIONS as err:
            log.error(err)
            return None
