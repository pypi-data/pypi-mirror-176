from flask import request, Flask
from jsonschema import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, HTTPException

from .extensions import response, ConflictException
from .monitoring import Monitoring

descriptions_to_log = [
    "Failed to decode JSON object",
    "The browser (or proxy) sent a request that this server could not understand.",
]


class ExceptionHandler:
    def __init__(self, monitoring: Monitoring):
        self.monitoring = monitoring

    """
        We use this method to allow logging for multiple monitoring stacks,
        as many apps could live under the same deployable unit.
    """

    def handle_bad_request(self, e):
        description_error = None

        if hasattr(e, "description"):
            if isinstance(e.description, ValidationError):
                description_error = str(e.description.message)
            else:
                if e.description in descriptions_to_log:
                    description_error = str(e.description)

        result_message = "Bad request"

        if description_error is not None:
            if request.method == "POST":
                self.monitoring.create(400, e=e)
            elif request.method == "PUT":
                self.monitoring.update(400, e=e)

            result_message = description_error

        return response({"Message": result_message}, 400)

    def handle_not_found(self, e):
        return response("", 404)

    def handle_bad_method(self, e):
        return response("", 405)

    def handle_conflict(self, e):
        return response("", 403)

    def handle_integrity(self, e):
        return response(
            {"Message": "Integrity error. Please check provided information"}, 400
        )

    def handle_any(self, e):
        if not isinstance(e, HTTPException):
            self.monitoring.general_error(e)
            return response({"Message": "Application error"}, 500)

        return response({"Message": "Application error"}, 500)


def register_errors(app: Flask, monitoring: Monitoring):
    handler = ExceptionHandler(monitoring)

    app.register_error_handler(BadRequest, handler.handle_bad_request)
    app.register_error_handler(405, handler.handle_bad_method)
    app.register_error_handler(KeyError, handler.handle_bad_request)
    app.register_error_handler(404, handler.handle_not_found)
    app.register_error_handler(ConflictException, handler.handle_conflict)
    app.register_error_handler(IntegrityError, handler.handle_integrity)
    app.register_error_handler(Exception, handler.handle_any)
