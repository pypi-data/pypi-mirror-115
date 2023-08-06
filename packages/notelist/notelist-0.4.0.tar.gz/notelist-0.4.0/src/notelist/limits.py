"""Requests module."""

from datetime import datetime
from functools import wraps
from typing import Callable

from flask import current_app, request
from werkzeug.exceptions import TooManyRequests

from notelist.responses import ResponseData


# Requests log: It stores the last time each client (by its address) made a
# request to each URL and method.
req_log = {}


def req_limit(min_sec: int) -> Callable:
    """Limit the number of requests per client, URL and method allowed.

    This is a decorator for view functions. If a client (based on its address)
    makes a request to a given URL and method and then makes a second request
    to the same URL and method less than `min_sec` seconds later, a HTTP 429
    error (Too Many Requests) response is returned.

    :param sec: Minimum number of seconds to wait between one request and
    another.
    """
    def wrapper1(f: Callable) -> Callable:
        @wraps(f)
        def wrapper2(*args, **kwargs) -> ResponseData:
            # If we are running the unit tests, then we don't apply the limit.
            if current_app.config.get("TESTING"):
                return f(*args, **kwargs)

            addr = request.remote_addr
            url = request.url
            met = request.method
            k = (addr, url, met)

            now = datetime.now()
            diff = (now - req_log[k]).seconds if k in req_log else None
            req_log[k] = now

            if diff is not None and diff < min_sec:
                raise TooManyRequests(retry_after=min_sec)

            return f(*args, **kwargs)

        return wrapper2

    return wrapper1
