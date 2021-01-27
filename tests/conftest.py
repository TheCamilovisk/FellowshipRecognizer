from pytest import fixture
from fellowship_recognizer import create_app


@fixture
def app():
    yield create_app()


@fixture
def cli(app):
    with app.test_client() as client:
        yield client
