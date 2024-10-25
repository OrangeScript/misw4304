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
                'email': fake.ascii_company_email(),
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

    