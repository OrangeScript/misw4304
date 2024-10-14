from sqlalchemy.exc import SQLAlchemyError
from src.commands.base_command import BaseCommand

from src.models.model import Banned
from src.utils.validations import is_valid_email


class getEmailFromBlacklistData(BaseCommand):
    def __init__(self, email: str):
        self.email = email

    def execute(self) -> dict:
        if not self.email:
            return {
                "response": {"msg": "Invalid email"},
                "status_code": 400,
            }

        if not is_valid_email(self.email):
            return {
                "response": {"msg": "Invalid email"},
                "status_code": 400,
            }

        try:
            found_email = Banned.query.filter_by(email=self.email).first()
            if not found_email:
                return {
                    "response": {"found": False, "blocked_reason": None},
                    "status_code": 200,
                }

            return {
                "response": {
                    "found": True,
                    "blocked_reason": found_email.blocked_reason,
                },
                "status_code": 200,
            }

        except SQLAlchemyError as e:
            return {
                "response": {"msg": f"An unexpected error occurred: {e}"},
                "status_code": 500,
            }

        except Exception as e:
            return {
                "response": {"msg": f"An unexpected error occurred: {e}"},
                "status_code": 500,
            }
