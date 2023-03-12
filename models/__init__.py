from datetime import datetime
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # user balance
    balance = db.relationship('Balance', backref='user')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'is_authenticated': self.is_authenticated
        }


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(30), nullable=False)  # BTCUSDT щоб брати з апі
    abbreviation = db.Column(db.String(30))  # BTC-USDT для юзера

    balances = db.relationship('Balance', backref='coin')

    def to_dict(self):
        return {
            'id': self.id,
            'abbreviation': self.abbreviation,
        }


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'))

    def to_dict(self):
        coin = Coin.query.get(id=self.coin_id)
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={coin.index}'

        # https://www.binance.me/api/v3/ticker/price?symbols=%5B%22DOGEUSDT%22,%22BTCUSDT%22%5D

        return {
            'id': self.id,
            'amount': str(self.amount),
            'value': requests.get(url).json()
        }

