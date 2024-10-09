from src.errors.response_errors import baseResponseError
from src.commands.base_command import BaseCommand


class AddEmailToBlacklist(BaseCommand):
    def __init__(self, request_body: dict):
        self.request_body = request_body

    def execute(self) -> dict:
        try:
            request_body = self.request_body
            return {"response": request_body, "status_code": 201}
        except baseResponseError as e:
            raise e
