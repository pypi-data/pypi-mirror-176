from typing import Tuple

from flask_sqlalchemy import SQLAlchemy


def init_extensions() -> Tuple[SQLAlchemy]:
    db = SQLAlchemy()
    return (db,)
