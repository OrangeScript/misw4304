import pytest

from application import app
from src.models.model import db

@pytest.fixture(autouse=True, scope='session')
def flask_app():
    db_url = f"sqlite:///:memory:"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["TESTING"] = True
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app
        db.session.rollback()
        db.session.close()
        db.drop_all()

@pytest.fixture(scope='session')
def client(flask_app):
    return flask_app.test_client()
