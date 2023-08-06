import os
import sys
import json
import datetime
import traceback as _traceback
from urllib.parse import quote, unquote
from html import escape, unescape
from http.cookies import SimpleCookie
from cgi import FieldStorage


log_file = "log.log"
traceback = False


_SERVER = dict(os.environ)
arguments = FieldStorage()
arguments = {k: [_.value for _ in arguments[k]] if isinstance(arguments[k], list) else arguments[k].value for k in arguments}
_GET = arguments
_POST = arguments
_SESSION = SimpleCookie(_SERVER["HTTP_COOKIE"]) if "HTTP_COOKIE" in _SERVER else {}
_COOKIE = {k: v.value for k, v in _SESSION.items()}
_HEADERS = {k: v for k, v in _SERVER.items() if k not in [
    "DOCUMENT_ROOT",
    "HTTP_CONNECTION",
    "LANG",
    "CONTEXT_DOCUMENT_ROOT",
    "SERVER_SIGNATURE",
    "SERVER_SOFTWARE",
    "SERVER_PORT",
    "REMOTE_PORT",
    "SCRIPT_NAME",
    "SERVER_ADMIN",
    "LANGUAGE",
    "QUERY_STRING",
    "GATEWAY_INTERFACE",
    "REQUEST_URI",
    "SERVER_PROTOCOL",
    "PYTHONIOENCODING",
    "SERVER_ADDR",
    "LC_ALL",
    "SCRIPT_FILENAME",
    "PATH",
    "CONTEXT_PREFIX",
]}
__headers = {
    "Content-Type": "text/html; charset=utf-8"
}
__response = {
    "status_code": 200,
    "content": b""
}
PRINTED = {
    "STATUS": False,
    "HEADERS": False,
}


def obj_to_bytes(obj):
    if isinstance(obj, str):
        obj = obj.encode()
    elif not isinstance(obj, bytes):
        try:
            obj = json.dumps(obj)
        except:
            obj = str(obj)
        obj = obj.encode()
    return obj


def _print(obj):
    sys.stdout.buffer.write(obj_to_bytes(obj)+b"\n")


def log(obj):
    obj = obj_to_bytes(obj)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()
    open(log_file, "ab").write(now+b" "+obj+b"\n")


def set_status(code: int):
    if not PRINTED["STATUS"]:
        __response["status_code"] = code
    else:
        raise Exception("! status_code printed: {}, {}".format(
            PRINTED["STATUS"],
            __response["status_code"])
        )


def set_header(k, v):
    __headers[k] = v


def print(obj):
    __response["content"] += obj_to_bytes(obj)+b"\n"


def traceback():
    return escape(_traceback.format_exc()).replace("\n", "<br>\n")


def _generate_response():
    _print("{}: {}".format(
        "Status",
        __response["status_code"]
    ))
    PRINTED["STATUS"] = True
    for k, v in __headers.items():
        _print("{}: {}".format(
            k,
            v
        ))
    _print("")
    PRINTED["HEADERS"] = True
    _print(__response["content"])


def execute(main):
    def _execute(*args, **kwargs):
        try:
            main(*args, **kwargs)
        except:
            set_status(500)
            __response["content"] = traceback()
        finally:
            _generate_response()

    return _execute



