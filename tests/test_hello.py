from pytest import fixture
from fellowship_recognizer import create_app


@fixture
def app():
    yield create_app()


@fixture
def cli(app):
    with app.test_client() as client:
        yield client


def test_hello(cli):
    response = cli.get("/")
    assert response.status_code == 200

    data = response.json
    assert "Hello" in data.keys()
    assert "World!!!" == data["Hello"]
