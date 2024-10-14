from flask import Blueprint, jsonify, request
from src.middlewares.token import validate_token
from src.constants.urls import BLACKLIST_BLUEPRINT, BLACKLIST_BLUEPRINT_PREFIX
from src.models.dto import createBlacklistDTO
from src.middlewares.validation import validate_request_data
from src.commands.add_email import AddEmailToBlacklist
from src.commands.get_email_data import getEmailFromBlacklistData

blueprint = Blueprint(
    BLACKLIST_BLUEPRINT, __name__, url_prefix=BLACKLIST_BLUEPRINT_PREFIX
)


@blueprint.route("/", methods=["POST"])
@validate_token
@validate_request_data(createBlacklistDTO)
def add_email_to_blacklist():
    body = request.get_json()
    response = AddEmailToBlacklist(body).execute()
    return jsonify(response["response"]), response["status_code"]


@blueprint.route("/<string:email>", methods=["GET"])
@validate_token
def get_offer_data(email):
    command = getEmailFromBlacklistData(email=email)
    result = command.execute()
    return jsonify(result["response"]), result["status_code"]


@blueprint.route("/health", methods=["GET"])
def ping():
    return "Ok", 200
