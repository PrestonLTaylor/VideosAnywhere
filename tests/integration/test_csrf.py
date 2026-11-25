from flask.testing import FlaskClient
from app import app

TEST_ROUTE = "/csrf-test"

@app.route(TEST_ROUTE, methods=["POST"])
def csrf_test_route():
    return "", 200

# NOTE: Instead of testing every endpoint's CSRF we disable it for all client fixtures
# However, we use a test endpoint that has CSRF enabled and check that it does not accept the request with no CSRF token.
# This should would with every endpoint that requires CSRF.
def test_that_video_upload_start_returns_ok_with_a_random_upload_id(client: FlaskClient):
    # Arrange
    client.application.config["WTF_CSRF_ENABLED"] = True

    # Act
    response = client.post(TEST_ROUTE)

    # Assert
    assert response.status_code == 400, "Response was not 400 Bad Request."