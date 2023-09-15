from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    app.register_blueprint(main)

    return app