import json
import sys
import aiohttp

from faf.api.client.client_base import BaseApiClient

if sys.version_info[:2] == (3, 5):
    class AioHttpClient(BaseApiClient):
        def make_session(self):
            return aiohttp.ClientSession()

        async def get(self, url, **kwargs):
            """
            Retrieve and deserialize the objects at the given url

            :param url: url to retrieve
            :param kwargs: additional arguments to be passed to the underlying implementation

            :return: A set of objects deserialized according to the schema
            """
            response = await self._session.get(self._base_url + url, headers=self._headers)
            decoded = json.loads(response.content.decode('utf-8'))
            if isinstance(decoded['data'], list):
                return map(self.deserialize_obj, decoded['data'])
            else:
                return self.deserialize_obj(decoded['data'])

        async def post(self, url, data, **kwargs):
            """
            Serialize and POST the given objects to the given url
            :param url: url to POST to
            :param data: objects to send
            :param kwargs: arguments for the underlying implementation
            :return: response object
            """
            return await self._session.post(self._base_url + url, data=data, **kwargs)

        async def put(self, url, **kwargs):
            """
            Serialize and PUT the given objects to the given url
            :param url: url to POST to
            :param data: objects to send
            :param kwargs: arguments for the underlying implementation
            :return: response object
            """
            return await self._session.put(self._base_url + url, **kwargs)

        async def delete(self, url, **kwargs):
            """
            Delete the object at the given url
            :param url: url to send DELETE to
            :param kwargs: additional arguments to the underlying implementation
            :return: response object
            """
            return await self._session.delete(self._base_url + url, **kwargs)

