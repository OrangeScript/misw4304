from src.commands.base_command import BaseCommand
from src.errors.response_errors import baseResponseError


class getEmailFromBlacklistData(BaseCommand):
    def __init__(self, email: str):
        self.email = email

    def execute(self) -> dict:
        try:
            email = self.email
            return {"response": email, "status_code": 200}
        except baseResponseError as e:
            raise e
