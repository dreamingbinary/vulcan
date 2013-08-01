from twisted.python.failure import Failure
from twisted.web.error import Error
from twisted.web import http

from twisted.python import log
from vulcan.utils import safe_format


class CommunicationFailed(Exception):
    pass


class RateLimitReached(Exception):
    def __init__(self, request_params, limit):
        Exception.__init__(self, safe_format(
            ('Limit of {n} {method} requests in {period} seconds '
             'for path "{path}" has been reached'),
            n=limit["threshold"],
            method=request_params["method"],
            period=limit["period"],
            path=request_params["uri"]))


class AuthorizationFailed(Error):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__


# http://tools.ietf.org/html/rfc6585
TOO_MANY_REQUESTS = 429

RESPONSES = {TOO_MANY_REQUESTS: "Too Many Requests"}
RESPONSES.update(http.RESPONSES)
