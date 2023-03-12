from os import environ

from flask import Flask
from flask_migrate import Migrate

from views import blueprint
from models import db
from service import login_manager
from rest import api, UserApi, CoinApi, BalanceApi


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    # adding database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{environ.get("DB_USERNAME")}:{environ.get("DB_PASSWORD")}'\
                                            '@localhost/CRYPTEX'

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
    api.add_resource(BalanceApi, '/api/v1/balances')
    api.init_app(app)

    return app

