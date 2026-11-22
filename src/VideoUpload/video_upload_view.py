from flask import Flask, render_template, make_response, jsonify, request
from VideoUpload.video_upload_form import VideoUploadForm
from werkzeug.utils import secure_filename
import os

# TODO: Ensure modular monolith structure being used.
def add_video_upload_routes(app: Flask) -> None:
    """
    Adds the route "/video/upload" to use the `video_upload_get` function on GET requests.
    Adds the route "/video/upload" to use the `video_upload_post` function on POST requests.
    """
    app.add_url_rule("/video/upload", view_func=video_upload_get, methods=["GET"])
    app.add_url_rule("/video/upload", view_func=video_upload_post, methods=["POST"])

def video_upload_get() -> str:
    form = VideoUploadForm()

    return render_template("video_upload.html", form=form)

def video_upload_post():
    form = VideoUploadForm()

    if form.validate():
        video_data = form.raw_video.data

        # TODO: DB and video encoding, saving to file is temporary.
        os.makedirs("./src/static/videos/", exist_ok=True)

        # NOTE: Use secure_filename to ensure no bad filename that is unsupported can be used.
        video_path = f"./src/static/videos/{secure_filename(video_data.filename)}"

        video_data.save(video_path)

        created_response = make_response(jsonify({}), 201)
        # NOTE: [6:] removes the ./src/ from the video_path
        created_response.headers["Location"] = f"{request.root_url}{video_path[6:]}"

        return created_response
    else:
        return make_response(jsonify({"errors": form.errors}), 400)