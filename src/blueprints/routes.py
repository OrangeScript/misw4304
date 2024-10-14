from flask import Blueprint, jsonify, request
from src.models.dto import createBlacklistDTO
from src.middlewares.validation import validate_request_data
from src.commands.add_email import AddEmailToBlacklist
from src.commands.get_email_data import getEmailFromBlacklistData
from src.commands.health_check import HealthCheck
from functools import wraps

blueprint = Blueprint(
    'operations', __name__
)

PREDEFINED_TOKEN = "predifined_token"

def validate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        token_parts = auth_header.split()
        if len(token_parts) != 2 or token_parts[0] != "Bearer":
            return jsonify({"error": "Invalid authorization header format"}), 401

        token = token_parts[1]

        if token != PREDEFINED_TOKEN:
            return jsonify({"error": "Unauthorized"}), 403

        return f(*args, **kwargs)

    return decorated_function

@blueprint.route('/ping', methods = ['GET'])
def health_check():
    print('hello world')
    return HealthCheck().execute()


@blueprint.route("/blacklists", methods=["POST"])
# @validate_request_data(createBlacklistDTO)
def add_email_to_blacklist():
    body = request.get_json()
    response = AddEmailToBlacklist(body).execute()
    return jsonify(response["response"]), response["status_code"]


@blueprint.route("/blacklists/<string:email>", methods=["GET"])
@validate_token
def get_offer_data(email):
    command = getEmailFromBlacklistData(email=email)
    result = command.execute()
    return jsonify(result["response"]), result["status_code"]


@blueprint.route("/health", methods=["GET"])
def ping():
    return "Ok", 200
