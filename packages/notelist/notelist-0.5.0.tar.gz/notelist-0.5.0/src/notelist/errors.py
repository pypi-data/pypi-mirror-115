"""Error handlers module."""

from flask import Flask
from marshmallow import ValidationError
from werkzeug.exceptions import (
    NotFound, MethodNotAllowed, TooManyRequests, InternalServerError)

from notelist.responses import (
    ResponseData, MV_URL_NOT_FOUND, MV_METHOD_NOT_ALLOWED, MV_VALIDATION_ERROR,
    MV_TOO_MANY_REQUESTS, MV_INTERNAL_SERVER_ERROR, MT_ERROR_URL_NOT_FOUND,
    MT_ERROR_METHOD_NOT_ALLOWED, MT_ERROR_VALIDATION,
    MT_ERROR_TOO_MANY_REQUESTS, MT_ERROR_INTERNAL_SERVER, get_response_data)


# Type
ValErrorData = dict[str, list[str]]


def not_found_handler(e: NotFound) -> ResponseData:
    """Handle 404 errors (Not Found).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(MV_URL_NOT_FOUND, MT_ERROR_URL_NOT_FOUND), 404


def method_not_allowed_handler(e: MethodNotAllowed) -> ResponseData:
    """Handle 405 errors (Method Not Allowed).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(
        MV_METHOD_NOT_ALLOWED, MT_ERROR_METHOD_NOT_ALLOWED), 405


def validation_error_handler(error: ValErrorData) -> ResponseData:
    """Handle validation errors (`marshmallow.ValidationError` exceptions).

    :param error: Object containing the error messages.
    :return: Response data dictionary.
    """
    fields = ", ".join([i for i in error.messages.keys()])
    return get_response_data(
        MV_VALIDATION_ERROR.format(fields), MT_ERROR_VALIDATION), 400


def too_many_requests_error_handler(e: TooManyRequests) -> ResponseData:
    """Handle 429 errors (Too Many Requests).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    u = "second" if e.retry_after == 1 else "seconds"
    mv = MV_TOO_MANY_REQUESTS.format(e.retry_after, u)

    return get_response_data(mv, MT_ERROR_TOO_MANY_REQUESTS), 429


def internal_server_error_handler(e: InternalServerError) -> ResponseData:
    """Handle 500 errors (Internal Server Error).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(
        MV_INTERNAL_SERVER_ERROR, MT_ERROR_INTERNAL_SERVER), 500


def register_error_handlers(app: Flask):
    """Register the error handlers.

    :param app: Flask application object.
    """
    for e, f in [
        (NotFound, not_found_handler),
        (MethodNotAllowed, method_not_allowed_handler),
        (ValidationError, validation_error_handler),
        (TooManyRequests, too_many_requests_error_handler),
        (InternalServerError, internal_server_error_handler)
    ]:
        app.register_error_handler(e, f)
