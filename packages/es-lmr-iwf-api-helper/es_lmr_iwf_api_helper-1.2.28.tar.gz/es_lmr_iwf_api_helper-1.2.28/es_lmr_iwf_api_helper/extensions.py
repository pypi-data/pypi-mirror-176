from datetime import date

from werkzeug.exceptions import HTTPException, NotFound
from flask import jsonify, make_response
from flask.json import JSONEncoder
from yoyo import read_migrations, get_backend


def response(data, status=200):
    if data == "":
        res = make_response(data, status)
    else:
        res = jsonify(data)
        res.status_code = status

    res.headers.set("Content-Type", "application/json")

    return res


def apply_migrations(uri, path):
    backend = get_backend(uri)
    migrations = read_migrations(path)

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


class LMRJSONEncoder(JSONEncoder):
    def default(self, o):
        try:
            if isinstance(o, date):
                return o.isoformat()
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, o)


class NotFoundException(NotFound):
    code = 404
    description = "The database record does not exist"


class ConflictException(HTTPException):
    code = 403
    description = "Duplicate database records are forbidden"
