import pandas as pd

from http import HTTPStatus
from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    request,
)

from flaskr.db import get_db

bp = Blueprint("iris", __name__, url_prefix="/iris")


@bp.route("/", methods=("GET",))
def iris() -> tuple[Response, HTTPStatus]:
    if request.method != "GET":
        return jsonify({"error": "Invalid method"}), HTTPStatus.METHOD_NOT_ALLOWED

    try:
        db = get_db()
        records = db.execute("SELECT * FROM iris").fetchall()
        return jsonify(records), HTTPStatus.OK
    except Exception as e:
        return __db_error(e)


@bp.route("/mean", methods=("GET",))
def mean() -> tuple[Response, HTTPStatus]:
    if request.method != "GET":
        return jsonify({"error": "Invalid method"}), HTTPStatus.METHOD_NOT_ALLOWED

    try:
        db = get_db()
        records = db.execute("SELECT * FROM iris").fetchall()
        df = (
            pd.DataFrame.from_records(records)
            .drop(columns=["id"])
            .groupby("species")
            .mean()
        )
    except Exception as e:
        return __db_error(e)

    return jsonify(df.to_dict()), HTTPStatus.OK


def __db_error(e: Exception) -> tuple[Response, HTTPStatus]:
    """Utility method, logs and returns an internal database error"""
    current_app.logger.error(f"Database error: {e}")
    return jsonify({"error": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR
