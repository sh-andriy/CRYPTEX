import requests
from decimal import Decimal

from flask import request, jsonify, url_for
from flask_restful import reqparse, Resource, Api, abort

from models import User, Coin, Balance
from models import db


api = Api()


class UserApi(Resource):
    def get(self, id: int = None):
        response = {}
        user = User.query.get(id)
        if user:
            response = user.to_dict()
        return {'user': response}, 200

    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            abort(422)  # missing arguments

        if User.query.filter_by(email=email).first() is not None:
            user = User.query.filter_by(email=email).first()
            if user.verify_password(password):
                return {'email': user.email}, 200, {'Location': f"{request.url_root}api/v1/users/{user.id}"}
            else:
                abort(401)  # wrong password

        user = User(email=email)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        return {'email': user.email}, 201, {'Location': f"{request.url_root}api/v1/users/{user.id}"}


class CoinApi(Resource):
    def get(self):
        coins = Coin.query.all()
        return [coin.to_dict() for coin in coins], 200


class BalanceApi(Resource):
    def get(self):
        balances = Balance.query.all()
        return [balance.to_dict() for balance in balances], 200

    def post(self):
        amount = request.json.get('amount')
        user_id = request.json.get('user_id')
        coin_id = request.json.get('coin_id')
        if amount is None or user_id is None or coin_id is None:
            abort(422)  # missing arguments

        balance = Balance(
            amount=Decimal(amount),
            user_id=user_id,
            coin_id=coin_id,
        )
        db.session.add(balance)
        db.session.commit()

        return {}, 201


