from flask import make_response
from flask_restful import abort
import traceback
import sys


def rest_exception(e):
    return abort(
        e.code if hasattr(e, "code") else 400,
        error=[e.data] if hasattr(e, "data") else [format_exception(e)],
    )


def exception_converter(e):
    return make_response(format_exception(e), 400)


def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(
        traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])
    )

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str
