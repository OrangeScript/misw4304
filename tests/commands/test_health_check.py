import pytest

from application import application
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from src.commands.health_check import HealthCheck
from src.commands.base_command import BaseCommand


class TestHealthCheck():
    def test_base_model_inherit(self):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = HealthCheck()
        assert isinstance(route, BaseCommand)
        
    def test_health_check(self):
        with application.test_client() as client:
            response = client.get('/health')
            print(response.json)
            assert response.status_code == 200
            assert response.json == ['Ok', 200]