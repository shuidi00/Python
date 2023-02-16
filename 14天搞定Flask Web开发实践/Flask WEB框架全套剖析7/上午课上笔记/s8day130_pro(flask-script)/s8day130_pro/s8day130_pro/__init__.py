from flask import Flask

from .views.account import ac


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ac)
    return app