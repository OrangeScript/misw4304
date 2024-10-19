from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify

from src.errors.response_errors import baseResponseError
from src.constants.urls import BLACKLIST_BLUEPRINT
from src.constants.system import (
    APP_HOST,
    APP_PORT,
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
   
with application.app_context():
    print(f"Host: {APP_HOST} Port: {APP_PORT} URL: {PRODUCTION_URL_DB}")
    application.config["SQLALCHEMY_DATABASE_URI"] = PRODUCTION_URL_DB
    print("Database setup completed successfully.")  
    db.init_app(application)
    db.create_all()
 
if __name__ == "__main__":
    try:
        application.run(host=APP_HOST, port=APP_PORT, debug=False)

    except Exception as e:
        print(f"Server startup failed: {e}")
