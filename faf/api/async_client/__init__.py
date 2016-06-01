import sys

if sys.version_info[:2] == (3, 5):
    from .async_client import AioHttpClient
