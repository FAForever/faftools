import requests

from .client_base import BaseApiClient


class RequestsApiClient(BaseApiClient):
    """
    Implementation of BaseApiClient using the Requests library
    """
    def make_session(self):
        return requests.Session()
