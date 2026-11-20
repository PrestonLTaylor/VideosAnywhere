from flask.testing import FlaskClient

def test_that_video_upload_page_is_accessable_as_html_using_get_request(client: FlaskClient):
    # Arrange

    # Act
    response = client.get("/video/upload")

    # Assert
    assert response.status_code == 200, "Response from the video upload page was not 200 OK."
    assert "text/html" in response.content_type, "Response from the video upload page was not a HTML file."