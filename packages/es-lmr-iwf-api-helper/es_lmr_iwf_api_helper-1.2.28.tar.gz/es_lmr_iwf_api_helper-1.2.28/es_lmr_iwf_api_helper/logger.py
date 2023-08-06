import logging
import os
from logging import Logger

from rfc5424logging import Rfc5424SysLogHandler

from es_lmr_iwf_api_helper.static_config import AppConfig


def build_logger(app_config: AppConfig):
    log_level = os.getenv("LOGGER_LEVEL")

    app_logger = logging.getLogger("api")

    result_log_level = logging.INFO
    if log_level == "DEBUG":
        result_log_level = logging.DEBUG
    elif log_level == "WARN":
        result_log_level = logging.WARN
    elif log_level == "ERROR":
        result_log_level = logging.ERROR

    app_logger.setLevel(result_log_level)

    if os.getenv("LOGGER") == "syslog":
        handler = setup_rfc5424_logger(
            app_config, os.getenv("SYSLOG_ADDRESS"), int(os.getenv("SYSLOG_PORT"))
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    app_logger.addHandler(handler)


def setup_rfc5424_logger(
    app_config: AppConfig, syslog_address: str = "127.0.0.1", syslog_port: int = 514
):
    return Rfc5424SysLogHandler(
        address=(syslog_address, syslog_port),
        enterprise_id=app_config.get_enterprise_id(),
        appname=app_config.get_app_name(),
        structured_data={
            "origin": {
                "enterpriseId": app_config.get_enterprise_id(),
                "software": app_config.get_app_name(),
                "swVersion": app_config.get_version(),
            }
        },
    )


def register_or_get_default_logger(app_config: AppConfig):
    if "exception" not in logging.root.manager.loggerDict:
        logger = logging.getLogger("exception")
        logger.setLevel(logging.WARN)
        logger.addHandler(setup_rfc5424_logger(app_config))

    return logging.getLogger("exception")


def log_config_error(logger: Logger, message: str):
    logger.critical(message, extra={"msgid": "CONFIG_ERROR"})
