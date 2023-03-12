from os import environ
import pytest
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from flask_login import login_user
from models import User, db

from app import create_test_app


@pytest.fixture(scope='session', name='app')
def fixture_app():
    """
    Fixture that initializes app for testing
    """
    app_test = create_test_app()
    app_test.config["TESTING"] = True
    load_dotenv()
    app_test.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    with app_test.app_context():
        db.create_all()
        yield app_test
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    """
    Fixture that initializes client for testing
    """
    return app.test_client()


@pytest.fixture()
def authenticated_user(app):
    """
    Fixture that logs in a user for testing.
    """
    with app.app_context():
        # create a test user
        user = User(
            email='test@example.com',
            password_hash=generate_password_hash('password')
        )
        # save the user to the database
        db.session.add(user)
        db.session.commit()
        # log in the user
        login_user(user)
        # return the user
        return user
