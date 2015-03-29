import json

from PyQt4.QtCore import *
from PyQt4.QtNetwork import *

from faftools.api import _get_NAM

class RestResponse(QObject):

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
        resData = str(self.reply.readAll())
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
            resp = json.loads(resData)

            self.done.emit(resp)

        self._finalize.emit(self)

class RestService:

    'Global set of all live RestResponse objects'
    responses = set()

    @staticmethod
    def _get(url):
        req = QNetworkRequest(QUrl(url))

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
