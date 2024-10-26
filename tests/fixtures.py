import pytest

from application import application as app
from src.constants.system import DEVELOP_URL_DB
from src.models.model import db


@pytest.fixture(autouse=True, scope="session")
def flask_app():
    db_url = DEVELOP_URL_DB
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["TESTING"] = True
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app
        db.session.rollback()
        db.session.close()
        db.drop_all()


@pytest.fixture(scope="session")
def client(flask_app):
    return app.test_client()
