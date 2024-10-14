import uuid

from datetime import datetime

from src.models.model import db, Banned
from src.errors.response_errors import baseResponseError
from src.commands.base_command import BaseCommand
from src.utils.validations import is_valid_email


class AddEmailToBlacklist(BaseCommand):
    def __init__(self, request_body: dict):
        self.request_body = request_body

    def check_app_id(self) -> bool:
        try:
            route_id = self.request_body.get("app_uuid")
            uuid.UUID(route_id, version=4)
            return True
        except ValueError:
            return False

    def check_email_in_list(self) -> bool:

        try:
            email = self.request_body.get("email")
            app_uuid = self.request_body.get("app_uuid")
            banned = Banned.query.filter_by(email=email, app_uuid=app_uuid).first()
            if banned:
                return False
            return True

        except ValueError:
            return False

    def execute(self) -> dict:
        request_body = self.request_body
        email = request_body["email"]
        if not is_valid_email(email):
            return {
                "response": {"msg": "Invalid email"},
                "status_code": 400,
            }

        if not self.check_app_id():
            return {
                "response": {"msg": "Invalid App ID"},
                "status_code": 400,
            }

        if not self.check_email_in_list():
            return {
                "response": {"msg": "Email already in blacklist"},
                "status_code": 404,
            }

        try:
            session = db.session()

            new_banned = Banned(
                email=email,
                app_uuid=request_body["app_uuid"],
                blocked_reason=request_body["blocked_reason"],
                created_at=datetime.now(),
            )
            try:
                session.add(new_banned)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e

            return {
                "response": f"New email {email} added to blacklist",
                "status_code": 201,
            }

        except baseResponseError as e:
            raise e
