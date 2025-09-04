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
        current_app.logger.error(f"Database error: {e}")
        return jsonify(
            {"error": "Internal server error"}
        ), HTTPStatus.INTERNAL_SERVER_ERROR
