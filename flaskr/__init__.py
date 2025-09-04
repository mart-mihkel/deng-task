from flask import Flask
from typing import Any, Mapping

from . import db


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.logger.info("Configure app")
    # TODO: secrets with env
    app.config.from_mapping(
        IRIS_URL="https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv",
        DATABASE="dbname=iris user=dev password=dev host=localhost port=5432",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    app.logger.info("Start app")
    return app
