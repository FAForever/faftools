import json

from PyQt5.QtCore import *
from PyQt5.QtNetwork import *

from faftools.api import _get_NAM

class RestResponse(QObject):

    class RestError(Exception):
        def __init__(self, http_code, response):
            super(RestResponse.RestError, self).__init__(http_code, response)

            self.http_code = http_code
            self.response = response

    error = pyqtSignal(int, object)
    done = pyqtSignal(object)
    progress = pyqtSignal(int, int)

    _finalize = pyqtSignal(object)

    def __init__(self, reply):
        super(RestResponse, self).__init__()

        self.reply = reply
        reply.finished.connect(self._onFinished)
        reply.downloadProgress.connect(self._onProgress)

    def _onProgress(self, recv, total):
        self.progress.emit(recv, total)

    def _onFinished(self):
        resData = bytes(self.reply.readAll()).decode()
        if self.reply.error():
            http_code = self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            if len(resData) == 0:
                self.error.emit(http_code, self.reply.errorString())
            else:
                try:
                    self.error.emit(http_code, json.loads(resData)['message'])
                except (ValueError, KeyError): # Non-json response -> Server error
                    self.error.emit(http_code, resData)

        else:
            resp = json.loads(str(resData))

            self.done.emit(resp)

        self._finalize.emit(self)

    def wait(self, progress_cb=None):
        """
        Waits (doesn't block events) and returns response as deserialized json.

        Errors get raised.
        """

        if progress_cb:
            self.progress.connect(progress_cb)

        result = None

        loop = QEventLoop()

        def hack_callback(*args):
            nonlocal result

            result = args

            loop.exit(0)

        self.done.connect(hack_callback)
        self.error.connect(hack_callback)

        loop.exec()

        if len(result) == 1:
            return result
        else:
            raise self.RestError(*result)

def make_urlquery(**url_kwargs):
    query = QUrlQuery()

    if len(url_kwargs) > 0:
        query.setQueryItems(url_kwargs.items())

    return query

class RestService:

    'Global set of all live RestResponse objects'
    responses = set()

    @staticmethod
    def _get(url, **url_kwargs):
        url = QUrl(url)
        url.setQuery(make_urlquery(**url_kwargs))

        req = QNetworkRequest(url)

        return RestService._build_response(_get_NAM().get(req))

    @staticmethod
    def _post(url, post_data):
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        return RestService._build_response(
            _get_NAM().post(req, json.dumps(post_data).encode()))

    @staticmethod
    def _build_response(request):
        response = RestResponse(request)

        RestService.responses.add(response)

        response._finalize.connect(RestService._cleanup_response)

        return response


    @staticmethod
    def _cleanup_response(response):
        RestService.responses.remove(response)
