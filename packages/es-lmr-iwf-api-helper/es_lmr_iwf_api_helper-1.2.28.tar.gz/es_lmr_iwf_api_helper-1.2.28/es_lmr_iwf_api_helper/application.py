import os
import time
from typing import Tuple
from flask import g, request

from prometheus_client import (
    CollectorRegistry,
    multiprocess,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from yoyo import get_backend, read_migrations

from es_lmr_iwf_api_helper.config import parse_config_file, set_common_env
from es_lmr_iwf_api_helper.errors import register_errors
from es_lmr_iwf_api_helper.extensions import LMRJSONEncoder
from flask import Flask, Response

from es_lmr_iwf_api_helper.logger import build_logger
from es_lmr_iwf_api_helper.monitoring import Monitoring
from es_lmr_iwf_api_helper.static_config import AppConfig


def apply_migrations(uri: str, path: str):
    backend = get_backend(uri)
    migrations = read_migrations(path)

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def make_app(
    app_config: AppConfig, default_path: str, migrations_path: str, error_handler=True
) -> Tuple[Flask, Monitoring]:
    app = Flask(__name__, instance_relative_config=False)
    app.json_encoder = LMRJSONEncoder

    content = parse_config_file(app_config, default_path)
    set_common_env(app_config, content)

    build_logger(app_config)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_DSN")
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["REDIS_UDS"] = os.getenv("REDIS_UDS")
    app.config["REDIS_HOST"] = os.getenv("REDIS_HOST")
    app.config["REDIS_PORT"] = (
        int(os.getenv("REDIS_PORT")) if os.getenv("REDIS_PORT") else None
    )

    if os.getenv("PY_ENV") in ["dev", "test"]:
        apply_migrations(
            os.getenv("DB_DSN").replace("+pymysql", ""),
            migrations_path,
        )

    monitoring = Monitoring(app_config)

    if error_handler:
        register_errors(app, monitoring)

    @app.route("/metrics")
    def metrics():
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)

        return Response(data, mimetype=CONTENT_TYPE_LATEST)

    @app.before_request
    def before_request():
        if request.path != "/metrics":
            g.start_time = time.time()

    @app.after_request
    def after_request(response: Response):
        if "start_time" in g and response is not None:
            monitoring.response_information(
                int((time.time() - g.start_time) * 1000), response
            )

        response.headers.set("X-API-VERSION", app_config.get_swagger_api_version())

        return response

    return app, monitoring
