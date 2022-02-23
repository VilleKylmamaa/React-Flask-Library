import json
import os
from flask import Flask, Response, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # add CLI commands
    from . import models
    from . import api
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.delete_db_command)
    app.cli.add_command(models.insert_initial_data)
    app.register_blueprint(api.api_bp)

    # API start route
    from .utils import LibraryBuilder
    @app.route("/api/", methods=["GET"])
    def entry():
        body = LibraryBuilder()
        body.add_namespace("library", "/api/")
        body.add_control_get_books()
        return Response(
            json.dumps(body, indent=4),
            200,
            mimetype="application/vnd.mason+json"
        )
    
    return app


