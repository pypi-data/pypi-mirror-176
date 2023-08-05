import logging
from typing import Dict
import requests
logger = logging.getLogger(__name__)


class Client:
    TIMEOUT_IN_SEC = 5

    def __init__(self, function_name: str) -> None:
        assert function_name, "Function name is not provided!"
        self._endpoint = f'https://{function_name}.azurewebsites.net/api'

    def _check_request_status(request):
        if not request.ok:
            logger.error(request.content)
        request.raise_for_status()
        return request

    def get(self, params):
        assert isinstance(params, Dict)
        r = requests.get(self._endpoint, timeout=self.TIMEOUT_IN_SEC, params=params)
        return self._check_request_status(r)

    def post(self, params=None, json=None):
        assert isinstance(params, Dict) or isinstance(json, Dict)
        r = requests.post(self._endpoint, timeout=self.TIMEOUT_IN_SEC, params=params, json=json)
        return self._check_request_status(r)
