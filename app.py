from sqlalchemy.exc import SQLAlchemyError
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify
from sys import argv

from waitress import serve
from src.errors.response_errors import baseResponseError
from src.constants.urls import BLACKLIST_BLUEPRINT
from src.constants import DEVELOP_ARGS, PRODUCTION_ARGS
from src.constants.system import (
    APP_HOST,
    APP_PORT,
    APP_THREADS,
    DEVELOP_URL_DB,
    PRODUCTION_URL_DB,
)
from src.blueprints.routes import blueprint
from src.models.model import db

application = Flask(__name__)

application.register_blueprint(blueprint, name=BLACKLIST_BLUEPRINT)

application.wsgi_app = ProxyFix(application.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@application.errorhandler(Exception)
def handle_unexpected_error(error):
    response = jsonify({"error": f"An unexpected error occurred: {str(error)}"})
    return response, 500


@application.errorhandler(baseResponseError)
def handle_offer_creation_error(error):
    response = jsonify({"error": error.message})
    return response, error.status_code


def setup_database(db_url):
    try:
        with application.app_context():
            application.config["SQLALCHEMY_DATABASE_URI"] = db_url
            db.init_app(application)
            db.create_all()
            print("Database setup completed successfully.")
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database setup failed: {e}")


def setup_develop_environment():
    setup_database(DEVELOP_URL_DB)
    print(f"Server started on development mode at http://{APP_HOST}:{APP_PORT}")
    application.run(host=APP_HOST, port=APP_PORT, debug=True)


def setup_production_environment():
    print(f"Host: {APP_HOST} Port: {APP_PORT} URL: {PRODUCTION_URL_DB}")
    setup_database(PRODUCTION_URL_DB)    
    print(f"Server started on production mode at http://{APP_HOST}:{APP_PORT}")
    serve(application, host=APP_HOST, port=APP_PORT, threads=APP_THREADS)


if __name__ == "__main__":
    try:
        if len(argv) > 1 and argv[1] == DEVELOP_ARGS:
            print("Running in development mode.")
            setup_develop_environment()
        if len(argv) > 1 and argv[1] == PRODUCTION_ARGS:
            setup_production_environment()

        environments = [DEVELOP_ARGS, PRODUCTION_ARGS]
        print(f"No environment specified: {str(environments)}. Exiting.")

    except Exception as e:
        print(f"Server startup failed: {e}")
