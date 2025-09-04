import os

from flask import Flask
from typing import Any, Mapping

from . import db
from . import iris

DEV_SECRET_KEY = "dev"
SECRET_KEY = os.getenv("SECRET_KEY", DEV_SECRET_KEY)

DEV_PG_URL = "dbname=iris user=admin password=admin host=localhost port=5432"
PG_URL = os.getenv("PG_URL", DEV_PG_URL)


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.logger.info("Configure app")
    app.config.from_mapping(
        IRIS_URL="https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv",
        SECRET_KEY=SECRET_KEY,
        PG_URL=PG_URL,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(iris.bp)

    app.logger.info("Start app")
    return app
