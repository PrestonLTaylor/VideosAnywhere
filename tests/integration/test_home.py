from flask.testing import FlaskClient

def test_that_home_page_is_accessable_as_html_at_root_directory(client: FlaskClient):
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200, "Response from the home page was not 200 OK."
    assert "text/html" in response.content_type, "Response from the home page was not a HTML file."
