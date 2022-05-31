from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import InternalServerError

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect - Persons Location Consumer", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.errorhandler(NoResultFound)
    def handle_not_found(e):
        return {
            "error": "Not Found"
        }, 404

    @app.errorhandler(InternalServerError)
    def internal_server_error(e):
        return {
            "error": "Internal Server Error",
            "detail": e.original_exception
        }

    return app
