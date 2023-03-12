from logging.handlers import RotatingFileHandler  # pylint: disable=W0611
from os import environ
import logging
from flask import Flask
from flask_migrate import Migrate

from views import blueprint
from models import db
from service import login_manager
from rest import api, UserApi, CoinApi, BalanceApi


def create_app():
    """
    Initialized app
    """

    logger = logging.getLogger()

    log_format = logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_log = logging.StreamHandler()
    console_log.setFormatter(log_format)
    console_log.setLevel('DEBUG')
    logger.addHandler(console_log)

    file_log = logging.handlers.RotatingFileHandler('logs.log', maxBytes=1024*1000)
    file_log.setFormatter(log_format)
    logger.addHandler(file_log)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'test_secret')

    # adding database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{environ.get("DB_USERNAME")}:'\
                                            f'{environ.get("DB_PASSWORD")}@localhost/CRYPTEX'

    app.register_blueprint(blueprint)

    # initialising database
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Flask_Login manager
    login_manager.init_app(app)
    login_manager.login_view = 'blueprint.login'

    api.add_resource(UserApi, '/api/v1/users', '/api/v1/users/<int:id>')
    api.add_resource(CoinApi, '/api/v1/coins')
    api.add_resource(BalanceApi, '/api/v1/balances', '/api/v1/balances/<int:id>')
    api.init_app(app)

    return app


def create_test_app():
    """
    Initialized app for testing
    """
    test_app = Flask(__name__)

    test_app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    test_app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
    test_app.register_blueprint(blueprint)

    db.init_app(test_app)
    migrate = Migrate(test_app, db)
    migrate.init_app(test_app, db)

    # Flask_Login manager
    login_manager.init_app(test_app)
    login_manager.login_view = 'blueprint.login'

    api.add_resource(UserApi, '/api/v1/users', '/api/v1/users/<int:id>')
    api.add_resource(CoinApi, '/api/v1/coins')
    api.add_resource(BalanceApi, '/api/v1/balances', '/api/v1/balances/<int:id>')
    api.init_app(test_app)

    return test_app
