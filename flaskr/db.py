import io
import click
import psycopg
import requests
import pandas as pd

from psycopg.rows import dict_row
from flask import Flask, current_app, g


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db() -> psycopg.Connection:
    if "db" not in g:
        g.db = psycopg.connect(current_app.config["PG_URL"], row_factory=dict_row)  # type: ignore

    return g.db


def close_db(_: BaseException | None = None):
    db: psycopg.Connection | None = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    current_app.logger.info("Initalize database")
    db = get_db()
    cur = db.cursor()

    current_app.logger.debug("Fetch iris dataset")
    r = requests.get(current_app.config["IRIS_URL"])
    if r.status_code != requests.codes.ok:
        current_app.logger.fatal("Failed to fetch iris dataset")
        exit(1)

    current_app.logger.debug("Wrangle iris dataset")
    df = pd.read_csv(io.StringIO(r.text))
    df["sepal_ratio"] = df["sepal_length"] / df["sepal_width"]
    df["petal_ratio"] = df["petal_length"] / df["petal_width"]

    current_app.logger.debug("Initalize schema")
    with current_app.open_resource("schema.sql") as f:
        cur.execute(f.read().decode("utf8"), prepare=False)

    current_app.logger.debug("Insert iris data")
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


@click.command("init-db")
def init_db_command():
    """Clear existing data, create and fill new tables."""
    init_db()
    click.echo("Initialized database")
