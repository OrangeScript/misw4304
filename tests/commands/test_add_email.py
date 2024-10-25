import pytest

from faker import Faker
from application import application
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from src.commands.add_email import AddEmailToBlacklist
from src.commands.base_command import BaseCommand


class TestHealthCheck():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []
        for i in range(5):
            body = {
                'email': fake.ascii_email(),
                'app_uuid': str(fake.uuid4()),
                'blocked_reason': fake.pystr(),
                'request_ip': fake.pystr()
            }
            request_bodies.append(body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = AddEmailToBlacklist(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_invalid_email(self, gen_request):
        # Test to ensure invalid email is caught
        route = AddEmailToBlacklist(gen_request[0])
        route.request_body['email'] = 'invalid_email'
        response = route.execute()
        assert response['status_code'] == 400
        assert response['response']['msg'] == 'Invalid email'

    def test_invalid_app_id(self, gen_request):
        # Test to ensure invalid app id is caught
        route = AddEmailToBlacklist(gen_request[1])
        route.request_body['app_uuid'] = 'invalid_app_id'
        response = route.execute()
        assert response['status_code'] == 400
        assert response['response']['msg'] == "Invalid App ID"

    def test_email_in_blacklist(self, gen_request):
        # Test to ensure email already in blacklist is caught
        route = AddEmailToBlacklist(gen_request[2])
        route.check_email_in_list = MagicMock(return_value=False)
        response = route.execute()
        assert response['status_code'] == 404
        assert response['response']['msg'] == "Email already in blacklist"

    def test_execute(self, gen_request):
        # Test to ensure execute method works as expected
        route = AddEmailToBlacklist(gen_request[3])
        
        with patch.object(BaseCommand, 'execute') as mock_execute:
            mock_execute.return_value = {'response': 'Success', 'status_code': 200}
            response = route.execute()
            assert response['status_code'] == 201
            assert response['response'] == f"New email {gen_request[3]['email']} added to blacklist"

    