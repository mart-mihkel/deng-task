import psycopg

from psycopg.rows import dict_row
from flask import Flask, current_app, g


def init_app(app: Flask):
    app.teardown_appcontext(close_db)


def get_db() -> psycopg.Connection:
    if "db" not in g:
        g.db = psycopg.connect(current_app.config["DATABASE"], row_factory=dict_row)  # type: ignore

    return g.db


def close_db(_: BaseException | None = None):
    db: psycopg.Connection | None = g.pop("db", None)
    if db is not None:
        db.close()
