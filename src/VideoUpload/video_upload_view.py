from flask import Flask, render_template
from VideoUpload.video_upload_form import VideoUploadForm

# TODO: Ensure modular monolith structure being used.
def add_video_upload_routes(app: Flask) -> None:
    """
    Adds the route "/video/upload" to use the `video_upload_get` function on GET requests.
    """
    app.add_url_rule("/video/upload", view_func=video_upload_get, methods=["GET"])

def video_upload_get() -> str:
    form = VideoUploadForm()

    return render_template("video_upload.html", form=form)