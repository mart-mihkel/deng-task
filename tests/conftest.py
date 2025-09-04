import pytest

from flask import Flask
from typing import Generator
from flaskr import create_app


@pytest.fixture
def app() -> Generator[Flask]:
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
