from io import BytesIO
from flask.testing import FlaskClient
import pytest
import os

@pytest.fixture
def valid_video() -> tuple[BytesIO, str]:
    """
    Returns a valid `FileMultiDict` tuple that is expected to pass video uploading validation.
    """

    # TODO: Use a valid mp4 video here when we implement stricter video validation.
    return (BytesIO(b"Test"), "valid.mp4")

def test_that_video_upload_page_is_accessable_as_html_using_get_request(client: FlaskClient):
    # Arrange

    # Act
    response = client.get("/video/upload")

    # Assert
    assert response.status_code == 200, "Response from the video upload page was not 200 OK."
    assert "text/html" in response.content_type, "Response from the video upload page was not a HTML file."

def test_that_video_upload_returns_bad_request_when_no_form_data_is_supplied(client: FlaskClient):
    # Arrange

    # Act
    response = client.post("/video/upload")

    # Assert
    assert response.status_code == 400, "Response from POST with no video file was not 400 Bad Request."
    assert "The CSRF token is missing" in response.text, "Response from POST did not set validation errors correctly."

def test_that_video_upload_returns_bad_request_when_no_csrf_token_is_supplied(client: FlaskClient, valid_video: tuple[BytesIO, str]):
    # Arrange
    test_form_data = {"raw_video": valid_video}

    # Act
    response = client.post("/video/upload", content_type="multipart/form-data", data=test_form_data)

    # Assert
    assert response.status_code == 400, "Response from POST with no video file was not 400 Bad Request."
    assert "The CSRF token is missing" in response.text, "Response from POST did not set validation errors correctly."

def test_that_video_upload_returns_bad_request_when_no_video_file_is_supplied(client: FlaskClient):
    # Arrange
    client.application.config["WTF_CSRF_ENABLED"] = False

    # Act
    response = client.post("/video/upload", content_type="multipart/form-data", data={})
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with no video file was not 400 Bad Request."
    assert "errors" in json, "Response from POST did not set validation errors correctly."
    assert "raw_video" in json["errors"], "Response did not validate that a missing video file is an error."

def test_that_video_upload_returns_bad_request_when_non_mp4_video_is_uploaded(client: FlaskClient):
    # Arrange
    client.application.config["WTF_CSRF_ENABLED"] = False

    test_form_data = {"raw_video": (BytesIO(b""), "invalid.mp3")}

    # Act
    response = client.post("/video/upload", content_type="multipart/form-data", data=test_form_data)
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with no video file was not 400 Bad Request."
    assert "errors" in json, "Response from POST did not set validation errors correctly."
    assert len(json["errors"]) == 1, "There should only be one validation error returned."
    assert "raw_video" in json["errors"], "Response from POST did not validate that a missing video file is an error."

# TODO: Tests involving invalid/bad file names to ensure correct handling.
def test_that_video_upload_returns_created_when_valid_mp4_video_file_is_uploaded(client: FlaskClient, valid_video: tuple[BytesIO, str]):
    # Arrange
    client.application.config["WTF_CSRF_ENABLED"] = False

    test_form_data = {"raw_video": valid_video}

    expected_url_for_video = f"http://localhost/static/videos/{valid_video[1]}"
    expected_path_for_video = f"./src/static/videos/{valid_video[1]}"

    # Act
    response = client.post("/video/upload", content_type="multipart/form-data", data=test_form_data)

    # Assert
    assert response.status_code == 201, "Response from POST with valid video file was not 201 Created."
    assert response.location == expected_url_for_video, "Response's Location header was not set to expected file path."
    assert os.path.isfile(expected_path_for_video), "Video file does not exist where it was expected."