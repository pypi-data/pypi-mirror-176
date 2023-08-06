import datetime

from werkzeug.exceptions import HTTPException

from es_lmr_iwf_api_helper.config import get_page, get_filter, get_depth, get_page_size
from es_lmr_iwf_api_helper.dao import CrudDao, OneToOneRelationDao
from es_lmr_iwf_api_helper.extensions import response

from flask import request, g, Blueprint
from flask_expects_json import expects_json

from es_lmr_iwf_api_helper.monitoring import Monitoring
from es_lmr_iwf_api_helper.static_config import AppConfig, ApiConfig


def check_org_and_user(monitor: Monitoring) -> bool:
    org_id = request.headers.get("X-ORG-ID")
    user_name = request.headers.get("X-USER-NAME")

    error_message = None
    if "/audit" not in request.path and "/health-check" not in request.path:
        if not org_id:
            error_message = (
                f"{request.method} {request.path} - X-ORG-ID invalid or absent"
            )

    if not user_name:
        error_message = (
            f"{request.method} {request.path} - X-USER-NAME invalid or absent"
        )

    if error_message:
        monitor.auth_error(error_message)
        return False

    g.org_id = org_id
    g.user_name = user_name

    return True


def check_user(monitor: Monitoring) -> bool:
    user_name = request.headers.get("X-USER-NAME")

    if not user_name:
        error_message = (
            f"{request.method} {request.path} - X-USER-NAME invalid or absent"
        )
        monitor.auth_error(error_message)
        return False

    g.user_name = user_name

    return True


def get_crud_bp(
    dao: CrudDao,
    app_config: AppConfig,
    api_config: ApiConfig,
    monitor: Monitoring,
    validate_org: bool = True,
    body_on_create: bool = True,
):
    routes = Blueprint("routes", __name__)

    @routes.before_request
    def validate_auth():
        if validate_org:
            if not check_org_and_user(monitor):
                return response("", 401)
        else:
            if not check_user(monitor):
                return response("", 401)

    @routes.route("/", methods=["GET"])
    def list_all():
        try:
            page = get_page(request.args.get("page"))
            size = get_page_size(app_config, request.args.get("pageSize"))

            data = dao.find_paged(page, size)
            monitor.list_all()

            return response(data)
        except HTTPException as e:
            monitor.list_all(e=e)
            raise e

    @routes.route("/audit", methods=["GET"])
    def list_audit():
        try:
            depth = get_depth(request.args.get("depth"))
            delta = datetime.timedelta(minutes=depth)

            data = dao.find_audit(
                datetime.datetime.now(tz=datetime.timezone.utc) - delta
            )
            monitor.audit()

            return response(data)
        except HTTPException as e:
            monitor.audit(e=e)
            raise e

    @routes.route("/", methods=["POST"])
    @expects_json(api_config.get_add_schema(), force=True, check_formats=True)
    def create():
        try:
            element = dao.create(g.data)
            monitor.create(data=element)

            if body_on_create:
                return response({"Ref": element["Ref"]}, 201)
            else:
                return response("", 201)
        except HTTPException as e:
            monitor.create(e=e)
            raise e

    @routes.route("/<element_id>", methods=["GET"])
    def find(element_id):
        try:
            element = dao.find_one(element_id)
            monitor.find(data=element)
            return response(element)
        except HTTPException as e:
            monitor.find(e=e, refs={"REF": element_id})
            raise e

    @routes.route("/<element_id>", methods=["DELETE"])
    def delete(element_id):
        try:
            element = dao.delete(element_id)
            monitor.delete(data=element)
            return response("", 204)
        except HTTPException as e:
            monitor.delete(e=e, refs={"REF": element_id})
            raise e

    @routes.route("/<element_id>", methods=["PUT"])
    @expects_json(api_config.get_edit_schema(), force=True, check_formats=True)
    def update(element_id):
        try:
            element = dao.update(element_id, g.data)
            monitor.update(data=element)
            return response("", 204)
        except HTTPException as e:
            monitor.update(e=e, refs={"REF": element_id})
            raise e

    @routes.route("/health-check", methods=["GET"])
    def health_check():
        try:
            dao.check_connectivity()
            if g.user_name != "system":
                monitor.health()

            return response({"Message": app_config.get_version()})
        except HTTPException as e:
            monitor.health(e=e)
            return response({"Message": app_config.get_version()}, 500)

    return routes


def get_one_to_one_bp(
    dao: OneToOneRelationDao,
    app_config: AppConfig,
    api_config: ApiConfig,
    monitor: Monitoring,
):
    one_to_one = Blueprint("one_to_one", __name__)

    @one_to_one.before_request
    def validate_auth():
        if not check_org_and_user(monitor):
            return response("", 401)

    @one_to_one.route("/audit", methods=["GET"])
    def list_audit():
        try:
            depth = get_depth(request.args.get("depth"))
            delta = datetime.timedelta(minutes=depth)

            data = dao.find_audit(
                datetime.datetime.now(tz=datetime.timezone.utc) - delta
            )
            monitor.audit()
            return response(data)
        except HTTPException as e:
            monitor.audit(e=e)
            raise e

    @one_to_one.route("/", methods=["GET"])
    def list_all():
        try:
            page = get_page(request.args.get("page"))
            size = get_page_size(app_config, request.args.get("pageSize"))

            data = dao.find_paged(page, size)
            monitor.list_all()

            return response(data)
        except HTTPException as e:
            monitor.list_all(e=e)
            raise e

    @one_to_one.route("/<element_id>", methods=["GET"])
    def find(element_id):
        try:
            element = dao.find_one(element_id)
            monitor.find(data=element)
            return response(element)
        except HTTPException as e:
            monitor.find(e=e, refs={"REF": element_id})
            raise e

    @one_to_one.route("/<element_id>", methods=["PUT"])
    @expects_json(api_config.get_edit_schema(), force=True, check_formats=True)
    def update(element_id):
        try:
            element = dao.update(element_id, g.data)
            monitor.update(data=element)
            return response("", 204)
        except HTTPException as e:
            monitor.update(e=e, refs={"REF": element_id})
            raise e

    return one_to_one
