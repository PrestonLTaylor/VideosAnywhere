from flask import Flask, render_template, make_response, jsonify, request
from VideoUpload.video_chunk_upload_form import VideoChunkUploadForm
from werkzeug.utils import secure_filename
import os
import random
import string
from werkzeug.datastructures import FileStorage

# TODO: Ensure modular monolith structure being used.
def add_video_upload_routes(app: Flask) -> None:
    """
    Adds the route "/video/upload" to use the `video_upload_get` function on GET requests.
    Adds the route "/video/upload/start" to use the `video_upload_start` function on POST requests.
    Adds the route "/video/upload/part" to use the `video_upload_part` function on POST requests.
    Adds the route "/video/upload/end" to use the `video_upload_end` function on POST requests.
    """
    app.add_url_rule("/video/upload", view_func=video_upload_get, methods=["GET"])
    app.add_url_rule("/video/upload/start", view_func=video_upload_start, methods=["POST"])
    app.add_url_rule("/video/upload/part", view_func=video_upload_part, methods=["POST"])
    app.add_url_rule("/video/upload/end", view_func=video_upload_end, methods=["POST"])

def video_upload_get() -> str:
    form = VideoChunkUploadForm()

    return render_template("video_upload.html", form=form)

# TODO: Improve google-style docstring for these endpoints.
def video_upload_start():
    """
    Initiates a multi-part upload with a client and returns an ID for the client to use when uploading chunks.
    """
    upload_id = ''.join(random.choices(string.ascii_letters, k=32))
    return make_response(jsonify({"video_upload_id": upload_id}), 200)

def video_upload_part():
    """
    Recieves a chunk of a video from a client and it's upload ID. Chunk are grouped together by their ID.
    """
    form = VideoChunkUploadForm()

    if form.validate():
        video_data: FileStorage = form.video_chunk.data

        # TODO: DB and video encoding, saving to file is temporary.
        os.makedirs("./src/static/videos/", exist_ok=True)

        # NOTE: Use secure_filename to ensure no bad filename that is unsupported can be used.
        assert form.video_upload_id.data is not None
        video_path = f"./src/static/videos/{secure_filename(form.video_upload_id.data)}.mp4"
        with open(video_path, "ab") as f:
            f.write(video_data.stream.read())

        return ("", 204)
    else:
        return make_response(jsonify({"errors": form.errors}), 400)

def video_upload_end():
    """
    Ends a multi-part upload with a client, signifying that the client has uploaded the whole video.
    The endpoint returns the location of where to access the uploaded video from the Location header.
    """
    data = request.json
    video_upload_id = data.get("video_upload_id")
    if video_upload_id:
        secure_video_upload_id = secure_filename(video_upload_id)

        # If the video file for the video upload id does not exist that means
        # an invalid video upload is was supplied.
        if not os.path.isfile(f"./src/static/videos/{secure_video_upload_id}.mp4"):
            return make_response(jsonify({"errors": {"video_upload_id": ["Invalid Upload ID was supplied."]}}), 400)

        created_response = make_response(jsonify({}), 201)
        created_response.headers["Location"] = f"{request.root_url}static/videos/{secure_video_upload_id}.mp4"

        return created_response
    else:
        return make_response(jsonify({"errors": {"video_upload_id": ["This field is required."]}}), 400)