import pytest
from app import app
from flask.testing import FlaskClient, FlaskCliRunner

@pytest.fixture()
def client() -> FlaskClient:
    """
    Returns a `FlaskClient` instance for the flask app during the test session.
    """
    return app.test_client()

@pytest.fixture()
def runner() -> FlaskCliRunner:
    """
    Returns a `FlaskCliRunner` instance for the flask app during the test session.
    """
    return app.test_cli_runner()