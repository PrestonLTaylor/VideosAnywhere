from flask import Flask
from home_view import add_home_routes
from healthcheck import add_healthcheck_routes
from VideoUpload.video_upload_view import add_video_upload_routes

def add_routes(app: Flask) -> None:
    """
    Adds all the routes for the front-end.
    """

    add_home_routes(app)
    add_healthcheck_routes(app)
    add_video_upload_routes(app)