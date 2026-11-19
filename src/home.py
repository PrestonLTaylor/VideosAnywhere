from flask import Flask, render_template

def add_home_routes(app: Flask) -> None:
    """
    Adds the route "/" to use the `home` function.
    """
    app.add_url_rule("/", view_func=home)

def home() -> str:
    """
    Displays the index.html inside the template folder for the home page.
    """
    return render_template("index.html")