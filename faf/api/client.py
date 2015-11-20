try:
    from .qt_client import QtApiClient as ApiClient
except ImportError:
    from .requests_client import RequestsApiClient as ApiClient
