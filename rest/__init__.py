from decimal import Decimal
import requests

from flask import request, current_app
from flask_restful import Resource, Api, abort

from models import User, Coin, Balance
from models import db


api = Api()


class UserApi(Resource):
    """
    Defines an API resource for creating a new user.

    This resource defines an API endpoint for creating a new user. The
    endpoint expects an email and password in the request body, and creates
    a new user with those credentials if they are valid.
    If a user with the same email address already exists, the endpoint
    returns an error response.

    Attributes:
        None

    Methods:
        get(), post().
    """

    def get(self, id: int = None):
        """
        This function gets a user by ID for flask loqin_require system

        This method queries the database for a user with the specified ID,
        and returns a dictionary representation of the user object if one is
        found. If no user is found, the method returns an empty dictionary.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            dict: A dictionary representation of the user object, or an empty
             dictionary if no user is found.
            int: The HTTP status code to return with the response.

        """

        response = {}
        user = User.query.get(id)
        if user:
            response = user.to_dict()
        return {'user': response}, 200

    def post(self):
        """
        This is a function that creates a user and return user if present

        This method creates a new user with the email and password provided
        in the request body, and returns a success response with the user's
        email address and the location of the newly created user in the API.

        If the email or password are missing from the request body,
         the method returns an error response.
        If a user with the same email address already exists in the
         database, the method returns an error response.

        Returns:
            dict: A dictionary containing the email address of the
                newly created user.
            int: The HTTP status code to return with the response.
            dict: A dictionary containing the Location header to
                include in the response.

        Raises:
            werkzeug.exceptions.UnprocessableEntity: If the email or
             password are missing from the request body.
            werkzeug.exceptions.Unauthorized: If the provided email and
             password do not match a user in the database.

        """

        current_app.logger.info(f"REST - Login request start with for "
                                f"email: {request.json.get('email')}")

        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            current_app.logger.info("REST - Failed missing arguments")
            abort(422)  # missing arguments

        if User.query.filter_by(email=email).first() is not None:
            current_app.logger.info(f"REST - User found for email {email}")
            user = User.query.filter_by(email=email).first()
            if user.verify_password(password):
                current_app.logger.info("REST - User password OK")
                return {'email': user.email}, 200, \
                    {'Location': f"{request.url_root}api/v1/users/{user.id}"}

            current_app.logger.info("REST - User password FAIL")
            abort(401)  # wrong password

        user = User(email=email)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        current_app.logger.info("REST - Login request end")
        return {'email': user.email}, 201, {'Location': f"{request.url_root}api/v1/users/{user.id}"}


class CoinApi(Resource):
    """
    Defines an API resource for retrieving a list of coins.

    This resource defines an API endpoint for retrieving a list of all
    coins in the database.The endpoint returns a list of coin dictionaries,
    each containing the coin's unique identifier, name, symbol, and current price.

    Attributes:
        None

    Methods:
        get().
    """

    def get(self):
        """
        Retrieves a list of all coins in the database

        Args:
            None

        Returns:
            A tuple containing a list of coin dictionaries and HTTP status code.
            Each dictionary represents a coin and contains the following keys:
            - id: The coin's unique identifier.
            - name: The coin's name.
            - symbol: The coin's symbol.
            - price: The current price of the coin.

        """

        coins = Coin.query.all()
        return [coin.to_dict() for coin in coins], 200


class BalanceApi(Resource):
    """
    Defines an API resource for handling balances CRUD operations.

    This class provides endpoints for creating, reading, updating, and
    deleting balance records in the database. It expects requests and
    returns responses in JSON format.

    Attributes:
        None

    Methods:
        get(), post(), put(), delete().
    """
    def get(self, id: int = None):
        """
        This function gets the balances for a user with the specified id,
        optionally filtered by date range.

        Args:
            id(int): The id of the user whose balances to retrieve

        Returns:
            Tuple containing a list of dictionaries with balance info and HTTP status code.
            Each dictionary contains the following keys:
            - id (int): The balance ID.
            - user_id (int): The user ID.
            - coin_id (int): The ID of the coin associated with the balance.
            - amount (Decimal): The amount of the coin held in the balance.
            - date_added (datetime): The date and time when the balance was added.

            If 'from_date' and/or 'to_date' parameters are provided in the request body,
            the balances will be filtered by the date range specified.

            If the balances are not empty, the function retrieves the
            latest price for the coins in the balances from Binance API
            and calculates the total value of each balance using these prices.

            The response status code is 200 if balances are found
            and status code is 404 if not.

        """
        from_date = request.json.get('from_date')
        to_date = request.json.get('to_date')

        balances = Balance.query.filter(Balance.user_id == id)
        if from_date:
            balances = balances.filter(Balance.date_added >= from_date)
        if to_date:
            balances = balances.filter(Balance.date_added <= to_date)

        coind_indexes = "%22,%22".join({balance.coin.index for balance in balances})
        if coind_indexes == '':
            return []
        binance_api_url = f"https://www.binance.me/api/v3/ticker/price" \
                          f"?symbols=%5B%22{coind_indexes}%22%5D"
        indexes = requests.get(binance_api_url, timeout=5).json()
        prices = {index['symbol']: Decimal(index['price']) for index in indexes}

        response = []
        for balance in balances:
            price = prices[balance.coin.index]
            response.append(
                {
                    **balance.to_dict(),
                    # 'value': '{:,.2f}'.format(price * balance.amount),
                    'value': f'{price * balance.amount:,.2f}'
                }
            )
        return response, 200

    def delete(self, id: int = None):
        """
        This function deletes the balance with the specified ID from
        the database using SQLAlchemy's query API. It then commits the
        transaction to the database to make the changes permanent.

        Args:
            id(int): The id of the balance to delete.

        Returns:
            Tuple containing an empty dictionary and HTTP status code.

            The response status code is 204 if the balances was deleted
            and 404 if balance with specified id was not found.
        """
        Balance.query.filter_by(id=id).delete()
        db.session.commit()
        return {}, 204

    def put(self, id: int = None):
        """
        Function that updates the balance

        This function retrieves the balance with specified ID in the database
        using SQLAlchemy's query API. It then updates the balance with the new
        amount and coin ID specified in the request JSON data.The updated balance
        is then added to the db session and committed to make the changes permanent.

        Args:
            id(int) The ID of the balance to update.

        Returns:
            Tuple containing a dictionary and HTTP status code.

            The response status code is 204 if the balances was updated
            and 404 if balance with specified id was not found.
        """
        balance = Balance.query.get(id)
        balance.amount = Decimal(request.json.get('amount'))
        balance.coin_id = request.json.get('coin_id')
        db.session.add(balance)
        db.session.commit()
        return balance.to_dict(), 201

    def post(self):
        """
        This function creates a new balance record.

        This function creates a new `Balance` record in the database
        using the information provided in the request JSON data. The request
        must include values for the `amount`, `user_id`, and `coin_id` fields,
        or a 422 Unprocessable Entity response will be returned.
        The `amount` value will be parsed as a decimal using the `Decimal`
        constructor. The `user_id` and `coin_id` values will be used to create
        a new `Balance` record, which will be added to the database session and
        committed to make the changes permanent.

        Args:
            None

        Returns:
            Tuple containing an empty dictionary and HTTP status code.

            The response will be an empty dictionary and a status code of 201,
            indicating that the record was successfully created.
        """
        amount = request.json.get('amount')
        user_id = request.json.get('user_id')
        coin_id = request.json.get('coin_id')
        if amount is None or user_id is None or coin_id is None:
            current_app.logger.info("REST - Failed missing arguments")
            abort(422)  # missing arguments

        balance = Balance(
            amount=Decimal(amount),
            user_id=user_id,
            coin_id=coin_id,
        )
        db.session.add(balance)
        db.session.commit()

        return {}, 201
