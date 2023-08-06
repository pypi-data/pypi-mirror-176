import logging
import os
import json
from typing import Optional

from flask import request, g, Response
from prometheus_client import Counter, Summary
from werkzeug.exceptions import HTTPException

from es_lmr_iwf_api_helper.static_config import AppConfig

request_counter = Counter(
    "http_requests",
    "HTTP requests served by the API",
    ["action", "method", "result", "api"],
)
request_time_ms = Summary(
    "http_requests_time",
    "Time spent processing requests",
    ["action", "method", "result", "api"],
)
response_size = Summary(
    "http_requests_size",
    "Size of responses in bytes",
    ["action", "method", "result", "api"],
)


def clean_exception_message(message: str) -> str:
    parts = message.split("\n")
    clean_parts = []
    index = 0
    for part in parts:
        part = part.strip()
        if part != "":
            if index == 0:
                part = part + "."

            clean_parts.append(part)
            index += 1

    return " ".join(clean_parts)


def get_structured_data(prefix: str, enterprise: str, data: dict, action: str):
    element = {}
    extra = {}

    for k, v in data.items():
        if k == "ELEMENT" and type(data[k]) == dict:
            for k2, v2 in data[k].items():
                if type(data[k][k2]) == list:
                    index = 1
                    for inner_element in data[k][k2]:
                        extra[f"{k2}-{index}"] = inner_element
                        index += 1
                else:
                    element[k2] = v2
        else:
            element[k] = v

    return {
        **{f"{action}{prefix}@{enterprise}": element},
        **extra,
    }


class Monitoring:
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.logger = logging.getLogger("api")

    def __add_to_dict(self, data: dict, refs: Optional[dict[str, str]] = None):
        app_data = data.copy()

        if "org_id" in g and "ORG-ID" not in data:
            app_data["ORG-ID"] = g.org_id
        if "user_name" in g:
            app_data["USER-NAME"] = g.user_name

        if refs:
            for k, v in refs.items():
                app_data[k] = v

        return app_data

    def auth_error(self, message: str, via: str, username: Optional[str] = None):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        if username:
            resulting_user = username
        elif "user_name" in g:
            resulting_user = g.user_name
        else:
            resulting_user = request.headers.get("X-USER-NAME", "")

        extra = {
            "msgid": "EXCEPTION_AUTH",
            "structured_data": {
                f"Exception{prefix}@{enterprise}": {
                    "ERROR-TYPE": "VALIDATION",
                    "ORG-ID": request.headers.get("X-ORG-ID", ""),
                    "USER-NAME": resulting_user,
                    "VIA": via,
                }
            },
        }

        if os.getenv("LOGGER") == "console":
            extra["message"] = message
            self.logger.warning(json.dumps(extra, default=str))
        else:
            self.logger.warning(message, extra=extra)

        g.cm_action = "AUTH"
        request_counter.labels(g.cm_action, request.method, "401", prefix).inc()

    def auth(self, via: str, username: str):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        extra = {
            "msgid": "AUTH",
            "structured_data": {
                f"Data{prefix}@{enterprise}": {
                    "ORG-ID": request.headers.get("X-ORG-ID", ""),
                    "USER-NAME": username,
                    "VIA": via,
                }
            },
        }

        if os.getenv("LOGGER") == "console":
            extra["message"] = "Logged in"
            self.logger.info(json.dumps(extra, default=str))
        else:
            self.logger.info("Logged in", extra=extra)

        g.cm_action = "AUTH"
        request_counter.labels(g.cm_action, request.method, "200", prefix).inc()

    def list_all(self, code: int = 200, e: Optional[HTTPException] = None):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        data = request.args.to_dict()
        data = self.__add_to_dict(data)

        extra = {
            "msgid": "LIST",
            "structured_data": {f"List{prefix}s@{enterprise}": data},
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                text = "Page was successfully retrieved from the database"
                if "page" in data:
                    text = f"Page {data['page']} was successfully retrieved from the database"

                self.logger.info(text, extra=extra)
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "LIST"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def audit(self, code: int = 200, e: Optional[HTTPException] = None):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        data = request.args.to_dict()
        data = self.__add_to_dict(data)

        extra = {
            "msgid": "AUDIT",
            "structured_data": {f"Audit{prefix}s@{enterprise}": data},
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info(
                    "Audit records were successfully retrieved from the database",
                    extra=extra,
                )
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "AUDIT"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def create(
        self,
        code: int = 201,
        data: Optional[dict] = None,
        e: Optional[HTTPException] = None,
        refs: Optional[dict[str, str]] = None,
    ):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        app_data = {}
        if data is not None:
            app_data["ELEMENT"] = data
        app_data = self.__add_to_dict(app_data, refs)

        extra = {
            "msgid": "CREATE",
            "structured_data": get_structured_data(
                prefix, enterprise, app_data, "Create"
            ),
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info(
                    "The database record was successfully created", extra=extra
                )
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "CREATE"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def update(
        self,
        code: int = 204,
        data: Optional[dict] = None,
        e: Optional[HTTPException] = None,
        refs: Optional[dict[str, str]] = None,
    ):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        app_data = {}
        if data is not None:
            app_data["ELEMENT"] = data
        app_data = self.__add_to_dict(app_data, refs)

        extra = {
            "msgid": "UPDATE",
            "structured_data": get_structured_data(
                prefix, enterprise, app_data, "Update"
            ),
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info(
                    "The database record was successfully updated", extra=extra
                )
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "UPDATE"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def find(
        self,
        code: int = 200,
        data: Optional[dict] = None,
        e: Optional[HTTPException] = None,
        refs: Optional[dict[str, str]] = None,
    ):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        app_data = {}
        if data is not None:
            app_data["ELEMENT"] = data
        app_data = self.__add_to_dict(app_data, refs)

        extra = {
            "msgid": "FIND",
            "structured_data": get_structured_data(
                prefix, enterprise, app_data, "Find"
            ),
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info(
                    "The database record was successfully retrieved", extra=extra
                )
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "FIND"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def delete(
        self,
        code: int = 204,
        data: Optional[dict] = None,
        e: Optional[HTTPException] = None,
        refs: Optional[dict[str, str]] = None,
    ):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        app_data = {}
        if data is not None:
            app_data["ELEMENT"] = data
        app_data = self.__add_to_dict(app_data, refs)

        extra = {
            "msgid": "DELETE",
            "structured_data": get_structured_data(
                prefix, enterprise, app_data, "Delete"
            ),
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info(
                    "The database record was successfully deleted", extra=extra
                )
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "DELETE"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def health(self, code: int = 200, e: Optional[HTTPException] = None):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        data = {}
        if "user_name" in g:
            data["USER-NAME"] = g.user_name

        extra = {
            "msgid": "HEALTH",
            "structured_data": get_structured_data(prefix, enterprise, data, "Health"),
        }

        if os.getenv("LOGGER") == "console":
            if not e:
                self.logger.info(json.dumps(extra, default=str))
            else:
                extra["message"] = clean_exception_message(str(e))
                self.logger.warning(json.dumps(extra, default=str))
        else:
            if not e:
                self.logger.info("Successfully performed a health check", extra=extra)
            else:
                self.logger.warning(clean_exception_message(str(e)), extra=extra)

        g.cm_action = "HEALTH"
        request_counter.labels(
            g.cm_action, request.method, str(code) if e is None else str(e.code), prefix
        ).inc()

    def response_information(self, time: float, response: Response):
        prefix, enterprise = self.app_config.get_logging_info_by_url(request.path)

        # If this is a health check request and the user is system, we don't log anything

        if request.path.endswith("/health-check") and g.user_name == "system":
            return

        action = "UNKNOWN"
        if "cm_action" in g:
            action = g.cm_action
        elif self.app_config.exists_api_by_url(request.path):
            action = "FIND"

        request_time_ms.labels(
            action, request.method, response.status_code, prefix
        ).observe(time)
        response_size.labels(
            action, request.method, response.status_code, prefix
        ).observe(response.content_length)

    def general_error(self, e: Exception):
        extra = {"msgid": "GENERAL_ERROR", "structured_data": {}}

        if os.getenv("LOGGER") == "console":
            extra["message"] = clean_exception_message(str(e))
            self.logger.error(json.dumps(extra, default=str))
        else:
            self.logger.error(clean_exception_message(str(e)), extra=extra)
