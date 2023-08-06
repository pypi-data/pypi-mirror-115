"""Requests module."""

from datetime import datetime
from functools import wraps
from typing import Callable

from flask import current_app, request
from werkzeug.exceptions import TooManyRequests

from notelist.tools import get_current_ts
from notelist.responses import ResponseData
from notelist.models.requests import Request


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
            # If we are running tests, then we don't apply the limit.
            if current_app.config.get("TESTING"):
                return f(*args, **kwargs)

            # Request data
            addr = request.remote_addr
            url = request.url
            met = request.method

            current_ts = get_current_ts()
            error = False

            # Get existing request if it exists or a new one
            req = Request.get(addr, url, met)

            # If the request exists, calculate the time difference between the
            # current time and the Last Modified time of the request (in
            # seconds).
            if req:
                now = datetime.fromtimestamp(current_ts)
                last_mod = datetime.fromtimestamp(req.last_modified_ts)
                diff = (now - last_mod).seconds

                if diff < min_sec:
                    error = True

                # Update request
                req.last_modified_ts = current_ts
            else:
                req = Request(address=addr, url=url, method=met)

            # Save request
            req.save()

            # Raise exception if the time difference is lower than "min_sec"
            if error:
                raise TooManyRequests(retry_after=min_sec)

            return f(*args, **kwargs)

        return wrapper2

    return wrapper1
