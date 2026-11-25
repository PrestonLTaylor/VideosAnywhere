from io import BytesIO
from flask.testing import FlaskClient
import pytest
import random

@pytest.fixture
def valid_video_chunk() -> tuple[BytesIO, str]:
    """
    Returns a valid `FileMultiDict` tuple that is expected to pass video uploading validation.
    """

    return (BytesIO(b"Test"), "valid.mp4")

def test_that_video_upload_page_is_accessable_as_html_using_get_request(client: FlaskClient):
    # Arrange

    # Act
    response = client.get("/video/upload")

    # Assert
    assert response.status_code == 200, "Response from the video upload page was not 200 OK."
    assert "text/html" in response.content_type, "Response from the video upload page was not a HTML file."

def test_that_video_upload_start_returns_ok_with_a_random_upload_id(client: FlaskClient):
    # Arrange
    random.seed(100)
    expected_video_upload_id = "hxOKMwPBexcWXrqNkjjsGYkXCUQiHgau"

    # Act
    response = client.post("/video/upload/start")
    json = response.get_json()

    # Assert
    assert response.status_code == 200, "Response from POST was not 200 OK."
    assert json is not None and "video_upload_id" in json, "Response did not contain a video upload ID."
    assert json["video_upload_id"] == expected_video_upload_id, "Response did not contain expected video upload ID."

def test_that_video_upload_part_returns_bad_request_when_no_form_data_is_supplied(client: FlaskClient):
    # Arrange

    # Act
    response = client.post("/video/upload/part")
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with no form was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."

def test_that_video_upload_part_returns_bad_request_when_no_video_upload_id_is_supplied(client: FlaskClient, valid_video_chunk: tuple[BytesIO, str]):
    # Arrange
    test_form_data = {"video_chunk": valid_video_chunk}

    # Act
    response = client.post("/video/upload/part", content_type="multipart/form-data", data=test_form_data)
    json = response.get_json()
    print(json)

    # Assert
    assert response.status_code == 400, "Response from POST with no video upload ID was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."
    assert len(json["errors"]) == 1, "Response from POST did not have correct number of validation errors."
    assert "video_upload_id" in json["errors"], "Response from POST did not have an error that indicates a missing video upload ID."

def test_that_video_upload_part_returns_bad_request_when_no_video_chunk_is_supplied(client: FlaskClient):
    # Arrange
    test_form_data = {"video_upload_id": "valid_id"}

    # Act
    response = client.post("/video/upload/part", content_type="multipart/form-data", data=test_form_data)
    json = response.get_json()
    print(json)

    # Assert
    assert response.status_code == 400, "Response from POST with no video chunk was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."
    assert len(json["errors"]) == 1, "Response from POST did not have correct number of validation errors."
    assert "video_chunk" in json["errors"], "Response from POST did not have an error that indicates a missing video chunk."

def test_that_video_upload_part_returns_bad_request_when_invalid_file_chunk_is_supplied(client: FlaskClient):
    # Arrange
    test_form_data = {"video_upload_id": "valid_id", "video_chunk": (BytesIO(b"Test"), "invalid.mp3")}

    # Act
    response = client.post("/video/upload/part", content_type="multipart/form-data", data=test_form_data)
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with invalid file chunk was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."
    assert len(json["errors"]) == 1, "Response from POST did not have correct number of validation errors."
    assert "video_chunk" in json["errors"], "Response did not validate that a missing video upload id is an error."

def test_that_video_upload_part_returns_no_content_when_valid_video_chunk_upload_form_is_supplied(client: FlaskClient, valid_video_chunk: tuple[BytesIO, str]):
    # Arrange
    test_form_data = {"video_upload_id": "valid_id", "video_chunk": valid_video_chunk}

    # Act
    response = client.post("/video/upload/part", content_type="multipart/form-data", data=test_form_data)

    # Assert
    assert response.status_code == 204, "Response from POST with valid video chunk upload form was not 204 No Content."


def test_that_video_upload_end_returns_unsupported_media_type_when_no_json_body_is_supplied(client: FlaskClient):
    # Arrange

    # Act
    response = client.post("/video/upload/end")

    # Assert
    assert response.status_code == 415, "Response from POST with no form was not 415 Unsupported Media Type."

def test_that_video_upload_end_returns_bad_request_when_no_video_upload_id_is_supplied(client: FlaskClient):
    # Arrange

    # Act
    response = client.post("/video/upload/end", content_type="application/json", json={})
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with no form was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."
    assert len(json["errors"]) == 1, "Response from POST did not have correct number of validation errors."
    assert "video_upload_id" in json["errors"], "Response did not validate that a missing video upload id is an error."

def test_that_video_upload_end_returns_bad_request_when_invalid_video_upload_id_is_supplied(client: FlaskClient):
    # Arrange
    # NOTE: For now, as there is no file with the id of invalid in the video storage, the video id is invalid.
    json_body = { "video_upload_id": "invalid" }

    # Act
    response = client.post("/video/upload/end", content_type="application/json", json=json_body)
    json = response.get_json()

    # Assert
    assert response.status_code == 400, "Response from POST with no form was not 400 Bad Request."
    assert json is not None and "errors" in json, "Response from POST did not have correct validation errors."
    assert len(json["errors"]) == 1, "Response from POST did not have correct number of validation errors."
    assert "video_upload_id" in json["errors"], "Response did not validate that a missing video upload id is an error."

def test_that_video_upload_end_returns_created_when_valid_video_upload_is_supplied(client: FlaskClient):
    # Arrange
    valid_video_upload_id = "valid_id"
    expected_location_header_value = f"http://localhost/static/videos/{valid_video_upload_id}.mp4"

    # Create a temp file with the same name as the video upload id (NOTE: Temporary)
    open(f"./src/static/videos/{valid_video_upload_id}.mp4", "a").close()

    json_body = { "video_upload_id": valid_video_upload_id }

    # Act
    response = client.post("/video/upload/end", content_type="application/json", json=json_body)
    location_header = response.headers.get("Location")
    print(response.text)

    # Assert
    assert response.status_code == 201, "Response from POST with valid video upload ID was not 201 Created."
    assert location_header is not None and location_header == expected_location_header_value, "Response from POST did not have expected location header."

def test_that_a_full_video_upload_is_successful_and_video_file_has_correct_data(client: FlaskClient, valid_video_chunk: tuple[BytesIO, str]):
    # Arrange

    # Act
    response_start = client.post("/video/upload/start")
    video_id = response_start.get_json()["video_upload_id"]

    response_chunk = client.post("/video/upload/part", content_type="multipart/form-data", data={"video_upload_id": video_id, "video_chunk": valid_video_chunk})
    response_end = client.post("/video/upload/end", content_type="application/json", json={ "video_upload_id": video_id })

    # Assert
    assert response_start.status_code == 200, "Response from start POST was not 200 OK."
    assert response_chunk.status_code == 204, "Response from POST with no form was not 204 No Content."
    assert response_end.status_code == 201, "Response from POST with no form was not 201 Created."
