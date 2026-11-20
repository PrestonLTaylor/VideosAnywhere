from flask import Flask
from home import add_home_routes
from healthcheck import add_healthcheck_routes

def add_routes(app: Flask) -> None:
    """
    Adds all the routes for the front-end.
    """

    add_home_routes(app)
    add_healthcheck_routes(app)