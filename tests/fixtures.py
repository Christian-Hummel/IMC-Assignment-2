
import pytest

from src.app import create_app
from src.model.agency import Agency
from tests.testdata import populate
from src.database import db

@pytest.fixture()
def app():
    app = create_app("sqlite:///")

    with app.app_context():
        db.create_all()


    yield app

@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def agency(app):

    with app.app_context():
        agency = Agency.get_instance()
        populate(agency)

        yield agency

