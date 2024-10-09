from typing import Union
from flask import request, jsonify
from functools import wraps
from enum import Enum


def validationTypeResponse(field, value, message):
    return {
        "field": field,
        "value": value,
        "message": message,
    }


def requiredFieldResponse(
    field,
    value,
):
    return {
        "field": field,
        "value": value,
    }


def validate_request_data(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data or data is None:
                return jsonify({"error": "No JSON data provided"}), 400

            missing_fields = [
                requiredFieldResponse(field, "Missing required fields")
                for field in required_fields
                if field not in data and not is_optional(required_fields[field], field)
            ]

            if missing_fields:
                return (
                    jsonify({"error": missing_fields}),
                    400,
                )

            errors = []

            status_code = 400
            for field, field_type in required_fields.items():
                value = data.get(field)

                if value is None:
                    continue
                if isinstance(field_type, type):
                    if issubclass(field_type, Enum):
                        if value not in [member.value for member in field_type]:
                            expected_values = [member.value for member in field_type]
                            exception_message = (
                                f"Expected one of {expected_values}, got '{value}'."
                            )
                            errors.append(
                                validationTypeResponse(field, value, exception_message)
                            )
                            status_code = 412

                    elif not isinstance(value, field_type):
                        expected_type = field_type.__name__
                        actual_type = type(value).__name__
                        exception_message = (
                            f"Expected '{expected_type}', got '{actual_type}'."
                        )
                        errors.append(
                            validationTypeResponse(field, value, exception_message)
                        )

            if errors:
                return jsonify({"error": errors}), status_code

            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_optional(typ, field):
    return getattr(typ, "__origin__", None) is Union and type(None) in getattr(
        typ, "__args__", ()
    )
