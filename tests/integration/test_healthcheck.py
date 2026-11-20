from flask.testing import FlaskClient

def test_that_healthcheck_returns_ok_with_no_errors_for_a_healthy_flask_app(client: FlaskClient):
    # Arrange
    expected_status = "ok"

    # Act
    response = client.get("/health")
    response_json = response.get_json()

    # Assert
    assert response.status_code == 200, "Response from the healthcheck was not 200 OK."
    assert response_json["status"] == expected_status, f"Status from healthcheck was not '{expected_status}'"
    assert not response_json["errors"], f"Errors returns from healthcheck was not empty"
