from datetime import datetime
import uuid
from faker import Faker
from src.constants.system import APP_TOKEN
from src.commands.add_email import AddEmailToBlacklist
from src.commands.base_command import BaseCommand
from src.models.model import db, Banned

fake = Faker()


class TestAddEmailToBlacklist:
    def setup_method(self):
        self.request_body = {
            "email": fake.email(),
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": fake.sentence(),
        }

        self.invalid_data = {
            "email": "bad.email@",
            "app_uuid": "invalid-uuid",
        }

        self.valid_headers = {"Authorization": f"Bearer {APP_TOKEN}"}

    def test_base_model_inherit(self):
        command = AddEmailToBlacklist(self.request_body)
        assert isinstance(command, BaseCommand)

    def test_add_email_to_blacklist(self, client):
        response = client.post(
            "/blacklists",
            json=self.request_body,
            headers=self.valid_headers,
            follow_redirects=True,
        )
        assert response.status_code == 201
        response_message = f"New email {self.request_body['email']} added to blacklist"
        assert response.get_json() == response_message

    def test_no_Authorization_header(self, client):
        response = client.post(
            "/blacklists",
            json=self.request_body,
            headers={},
            follow_redirects=True,
        )
        assert response.status_code == 403
        assert "error" in response.get_json()

    def test_bad_uuid_in_add_email_to_blacklist(self, client):
        bad_request = self.request_body.copy()
        bad_request["app_uuid"] = self.invalid_data["app_uuid"]

        response = client.post(
            "/blacklists",
            json=bad_request,
            headers=self.valid_headers,
            follow_redirects=True,
        )
        assert response.status_code == 400
        assert response.get_json()["msg"] == "Invalid App ID"

    def test_bad_email_in_add_email_to_blacklist(self, client):
        bad_request = self.request_body.copy()
        bad_request["email"] = self.invalid_data["email"]

        response = client.post(
            "/blacklists",
            json=bad_request,
            headers=self.valid_headers,
            follow_redirects=True,
        )
        assert response.status_code == 400
        assert response.get_json()["msg"] == "Invalid email"

    def test_add_email_already_in_blacklist(self, client):
        new_banned = Banned(
            email=self.request_body["email"],
            request_ip=fake.ipv4(),
            app_uuid=self.request_body["app_uuid"],
            blocked_reason=self.request_body["blocked_reason"],
            created_at=datetime.now(),
        )

        session = db.session()
        try:
            session.add(new_banned)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

        response = client.post(
            "/blacklists",
            json=self.request_body,
            headers=self.valid_headers,
            follow_redirects=True,
        )
        assert response.status_code == 404
