import os
import warnings

class Config:
    """
    A storage class for storing all the configuration for the flask application.

    Attributes:
        FRONTEND_PORT: A port number that the flask application will listen for requests from.
        SECRET_KEY: A secret key used to set flask's secret key. Required.
    """
    def __init__(self):
        frontend_port_env = os.getenv("FRONTEND_PORT") or ""
        self.FRONTEND_PORT = int(frontend_port_env) if frontend_port_env.isdecimal() else 5000

        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            warnings.warn("SECRET_KEY was not set, defaulting to a random value. This will break anything that relies on " \
            "flask's secret key being consistent", RuntimeWarning)
            import random
            import string
            secret_key = ''.join(random.choices(string.printable, k=32))

        self.SECRET_KEY = secret_key

    FRONTEND_PORT: int

    SECRET_KEY: str