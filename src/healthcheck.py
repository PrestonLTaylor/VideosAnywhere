from flask import Flask, jsonify, Response

def add_healthcheck_routes(app: Flask) -> None:
    """
    Adds the route "/health" to use the `healthcheck` function.
    """
    app.add_url_rule("/health", view_func=healthcheck)

def healthcheck() -> Response:
    """
    Performs a healthcheck on the flask app.
    A status of "ok" means that the flask app is healthy, any other status means the app is unhealthy.

    NOTE: This is actually a liveness for now, we should seperate them if needed in the future.

    Returns:
        The status of the flask app and any errors as a json response.
    """
    return jsonify({ "status": "ok", "errors": [] })