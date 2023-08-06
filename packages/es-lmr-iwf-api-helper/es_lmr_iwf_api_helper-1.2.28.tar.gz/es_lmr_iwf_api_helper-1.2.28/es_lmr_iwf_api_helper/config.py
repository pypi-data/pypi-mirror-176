import os
import sys

from flask import request
from logging import Logger
from typing import Optional

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from es_lmr_iwf_api_helper.logger import (
    log_config_error,
    register_or_get_default_logger,
)
from es_lmr_iwf_api_helper.static_config import AppConfig


def parse_config_file(app_config: AppConfig, basedir: str) -> ElementTree:
    default_file = (
        f"/opt/etherstack/config/{app_config.get_config_file()}/bootstrap.xml"
    )
    config_file = os.getenv("CONFIG_FILE")

    fallback_logger = register_or_get_default_logger(app_config)

    if config_file is None:
        if os.path.isfile(default_file):
            config_file = default_file
        current_path_bootstrap = os.path.join(basedir, "bootstrap.xml")
        if config_file is None:
            if os.path.isfile(current_path_bootstrap):
                config_file = current_path_bootstrap
            else:
                log_config_error(
                    fallback_logger, "No bootstrap.xml configuration file found"
                )
                sys.exit(1)

    try:
        return ElementTree.parse(config_file)
    except Exception as e:
        log_config_error(
            fallback_logger,
            f"Unable to parse XML configuration for: {config_file}. Exception is: {str(e)}",
        )
        sys.exit(1)


def val_or_exit(node: Element, key: str, logger: Logger):
    result = node.find(key)
    if result is None:
        log_config_error(
            logger,
            "Value does not exist on XML configuration file: " + key,
        )
        sys.exit(1)

    return result


def get_page_size(app_config: AppConfig, size: Optional[str]) -> int:
    if size is None:
        return app_config.get_default_page_size()

    if not size.isnumeric():
        return app_config.get_default_page_size()

    size = int(size)

    size = (
        app_config.get_min_page_size()
        if size < app_config.get_min_page_size()
        else size
    )
    size = (
        app_config.get_max_page_size()
        if size > app_config.get_max_page_size()
        else size
    )

    return size


def get_filter(filter_value: Optional[str]) -> Optional[str]:
    if filter_value is not None:
        return filter_value

    return None


def get_page(page_value: Optional[str]) -> int:
    if page_value is None:
        return 1

    if not page_value.isnumeric():
        return 1

    page_value = int(page_value)

    return 1 if page_value < 1 else page_value


def query_string_value(name: str) -> str:
    value = request.args.get(name)
    if value is None:
        return ""

    return value


def has_sort_field() -> bool:
    return "sortByField" in request.args


def is_sort_asc() -> bool:
    if "sortDirection" in request.args:
        if request.args.get("sortDirection") == "asc":
            return True

    return False


def get_depth(depth: Optional[str]) -> int:
    if depth is None:
        return 15

    if not depth.isnumeric():
        return 15

    depth = int(depth)

    depth = 120 if depth > 120 else depth
    depth = 15 if depth < 15 else depth

    return depth


def set_common_env(app_config: AppConfig, content: ElementTree):
    fallback_logger = register_or_get_default_logger(app_config)

    os.environ["TZ"] = "UTC"

    boot = val_or_exit(content.getroot(), "Boot", fallback_logger)

    syslog = val_or_exit(boot, "Syslog", fallback_logger)
    logger = val_or_exit(boot, "Logging", fallback_logger)
    redis = val_or_exit(boot, "Redis", fallback_logger)

    os.environ["LOGGER"] = val_or_exit(logger, "Provider", fallback_logger).text
    os.environ["LOGGER_LEVEL"] = val_or_exit(logger, "Level", fallback_logger).text
    os.environ["SYSLOG_ADDRESS"] = val_or_exit(syslog, "Address", fallback_logger).text
    os.environ["SYSLOG_PORT"] = val_or_exit(syslog, "Port", fallback_logger).text
    os.environ["DB_DSN"] = val_or_exit(boot, "Database", fallback_logger).text

    connection_type = val_or_exit(redis, "ConnectionType", fallback_logger).text
    if connection_type not in ["uds", "tcp"]:
        log_config_error(
            fallback_logger,
            f"Redis has an invalid connection type: {connection_type}",
        )
        sys.exit(1)

    if connection_type == "uds":
        os.environ["REDIS_UDS"] = val_or_exit(redis, "Uds", fallback_logger).text
        os.environ["REDIS_HOST"] = ""
        os.environ["REDIS_PORT"] = "0"
    elif connection_type == "tcp":
        os.environ["REDIS_UDS"] = ""
        os.environ["REDIS_HOST"] = val_or_exit(redis, "Host", fallback_logger).text
        os.environ["REDIS_PORT"] = val_or_exit(redis, "Port", fallback_logger).text
        if not os.environ["REDIS_PORT"].isnumeric():
            log_config_error(
                fallback_logger,
                f"REDIS_PORT isn't a numeric value: {os.environ['REDIS_PORT']}",
            )
            sys.exit(1)

    if not os.environ["LOGGER"] in ["syslog", "console"]:
        log_config_error(
            fallback_logger, f"Logger has an invalid value: {os.environ['LOGGER']}"
        )
        sys.exit(1)

    if not os.environ["LOGGER_LEVEL"] in ["DEBUG", "INFO", "WARN", "ERROR"]:
        log_config_error(
            fallback_logger,
            f"Logger level has an invalid value: {os.environ['LOGGER_LEVEL']}",
        )
        sys.exit(1)

    if os.environ["LOGGER"] == "syslog" and not os.environ["SYSLOG_PORT"].isnumeric():
        log_config_error(
            fallback_logger,
            f"Syslog logger requires SYSLOG_PORT variable: {os.environ['SYSLOG_PORT']}",
        )
        sys.exit(1)
