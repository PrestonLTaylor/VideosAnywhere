from flask import Flask
from home import add_home_routes

def add_routes(app: Flask) -> None:
    """
    Adds all the routes for the front-end.
    """

    add_home_routes(app)