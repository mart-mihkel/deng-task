import pandas as pd

from typing import cast
from http import HTTPStatus
from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    request,
)

from flaskr.db import get_db, wrangle_iris

bp = Blueprint("iris", __name__, url_prefix="/iris")


@bp.route("/", methods=("GET", "POST"))
def iris() -> tuple[Response, HTTPStatus]:
    if request.method == "GET":
        try:
            db = get_db()
            records = db.execute("SELECT * FROM iris").fetchall()
            return jsonify(records), HTTPStatus.OK
        except Exception as e:
            return __db_error(e)

    if request.method == "POST":
        try:
            return __upload_iris()
        except ValueError as e:
            current_app.logger.error(f"Database error: {e}")
            return jsonify({"error": f"{e}"}), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return __db_error(e)

    return jsonify({"error": "Invalid method"}), HTTPStatus.METHOD_NOT_ALLOWED


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


def __upload_iris() -> tuple[Response, HTTPStatus]:
    db = get_db()
    cur = db.cursor()

    df = pd.DataFrame.from_records(request.get_json())
    df = __validate_upload_input(df)
    df = wrangle_iris(df)

    query = """
        COPY iris (
            sepal_length, sepal_width, petal_length, petal_width,
            species, sepal_ratio, petal_ratio
        ) FROM STDIN (FORMAT CSV)
    """

    with cur.copy(query) as copy:
        copy.write(df.to_csv(header=False, index=False))

    cur.close()
    db.commit()

    return jsonify({"message": "Records uploaded"}), HTTPStatus.OK


def __validate_upload_input(df: pd.DataFrame) -> pd.DataFrame:
    required = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    extra = set(df.columns) - set(required)
    if extra:
        raise ValueError(f"Unexpected columns provided: {', '.join(extra)}")

    return cast(pd.DataFrame, df[required])
