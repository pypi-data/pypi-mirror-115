import os
import json
import datetime
from http.cookies import SimpleCookie
import cgi
import cgitb


class PythonCGI:
    def __init__(self, log_file: str = "log.log", traceback: bool = False, traceback_kwargs: dict = None):
        self.log_file = log_file
        self._server = dict(os.environ)
        arguments = cgi.FieldStorage()
        self._arguments = {k: [_.value for _ in arguments[k]] if isinstance(arguments[k], list) else arguments[k].value for k in arguments}
        self._session = SimpleCookie(self._server["HTTP_COOKIE"]) if "HTTP_COOKIE" in self._server else {}
        self._cookie = {k: v.value for k, v in self._session.items()}
        if traceback:
            if not traceback_kwargs:
                traceback_kwargs = {}
            cgitb.enable(**traceback_kwargs)

    @property
    def _GET(self):
        return self._arguments

    @property
    def _POST(self):
        return self._arguments

    @property
    def _COOKIE(self):
        return self._cookie

    @property
    def _SESSION(self):
        return self._session

    @property
    def _SERVER(self):
        return self._server

    def log(self, obj):
        if not isinstance(obj, bytes):
            try:
                obj = json.dumps(obj)
            except:
                obj = str(obj)
            obj = obj.encode()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()
        open(self.log_file, "ab").write(now+b" "+obj+b"\n")


