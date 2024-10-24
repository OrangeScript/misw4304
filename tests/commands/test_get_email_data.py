import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from src.commands.get_email_data import getEmailFromBlacklistData
from src.models.model import Banned


@pytest.fixture
def valid_email():
    return "test@example.com"


@pytest.fixture
def invalid_email():
    return "invalid-email"


@pytest.fixture
def banned_email():
    return "blocked@example.com"

# Test para cuando no se proporciona un correo
def test_execute_no_email():
    command = getEmailFromBlacklistData("")
    result = command.execute()
    assert result["status_code"] == 400
    assert result["response"]["msg"] == "Invalid email"


# Test para cuando el correo es inválido
def test_execute_invalid_email(invalid_email):
    command = getEmailFromBlacklistData(invalid_email)
    result = command.execute()
    assert result["status_code"] == 400
    assert result["response"]["msg"] == "Invalid email"


# Test cuando el correo no está bloqueado
@patch("src.models.model.Banned")
def test_execute_email_not_in_blacklist(mock_banned, valid_email):
    mock_banned.query.filter_by.return_value.first.return_value = None
    command = getEmailFromBlacklistData(valid_email)
    result = command.execute()
    assert result["status_code"] == 200
    assert result["response"]["found"] is False
    assert result["response"]["blocked_reason"] is None


# Test cuando el correo está bloqueado
@patch("src.models.model.Banned.query")
def test_execute_email_in_blacklist(mock_query, banned_email):
    mock_banned_instance = MagicMock()
    mock_banned_instance.email = banned_email
    mock_banned_instance.blocked_reason = "Spam"
    mock_query.filter_by.return_value.first.return_value = mock_banned_instance

    command = getEmailFromBlacklistData(banned_email)
    result = command.execute()
    assert result["status_code"] == 200
    assert result["response"]["found"] is True
    assert result["response"]["blocked_reason"] == "Spam"


# Test para manejar excepciones de SQLAlchemy
@patch("src.models.model.Banned.query")
def test_execute_sqlalchemy_error(mock_query, valid_email):
    mock_query.filter_by.side_effect = SQLAlchemyError("Database Error")

    command = getEmailFromBlacklistData(valid_email)
    result = command.execute()
    assert result["status_code"] == 500
    assert "An unexpected error occurred" in result["response"]["msg"]


# Test para manejar excepciones generales
@patch("src.models.model.Banned.query")
def test_execute_generic_exception(mock_query, valid_email):
    mock_query.filter_by.side_effect = Exception("Unexpected Error")

    command = getEmailFromBlacklistData(valid_email)
    result = command.execute()
    assert result["status_code"] == 500
    assert "An unexpected error occurred" in result["response"]["msg"]
