import requests

from .client_base import BaseApiClient


class RequestsApiClient(BaseApiClient):
    """
    Implementation of BasiApiClient using the Requests library
    """
    def make_session(self):
        return requests.Session()
