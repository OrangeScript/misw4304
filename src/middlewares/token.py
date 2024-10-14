from flask import jsonify, request
from functools import wraps

from src.constants.system import APP_TOKEN

PREDEFINED_TOKEN = APP_TOKEN


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
