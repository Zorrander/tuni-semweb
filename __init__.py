import os

from flask import Flask, jsonify
from flaskr.views import interface, endpoint, skills, grounding


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        TESTING=True,
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #  Register blueprints
    app.register_blueprint(interface.bp)
    app.register_blueprint(endpoint.bp)
    app.register_blueprint(grounding.bp)
    app.register_blueprint(skills.bp)
    app.add_url_rule('/', endpoint='index')

    return app
