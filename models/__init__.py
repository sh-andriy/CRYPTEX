from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Defines a SQLAlchemy model for a user account.

    This model defines a user account with an email address, password hash, date added,
    and active status. It inherits from the SQLAlchemy `Model` and `UserMixin` classes.

    Attributes:
        id (int): The primary key for the user account.
        email (str): The email address associated with the user account.
        password_hash (str): The hashed password for the user account.
        date_added (datetime): The date and time when the user account was created.
        is_active (bool): Indicates whether the user account is currently active.

    Relationships:
        balance (One-to-Many): Defines a one-to-many relationship between the `User` model
        and the `Balance` model. This relationship allows a user to have multiple balance
        objects associated with their account.

    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # user balance
    balance = db.relationship('Balance', backref='user')

    def hash_password(self, password):
        """
        Function that generates a hashed password for user

        This function generates a secure hashed password using the provided password and the
        'sha256' algorithm. The hashed password is then stored in the user object's 'password_hash'
        attribute.

        Args:
            password (str): The plaintext password to hash.
        """

        self.password_hash = generate_password_hash(password, 'sha256')

    def verify_password(self, password):
        """
        Function that verify a user's password

        This function checks whether the provided password matches the hashed password stored in
        the user object's 'password_hash' attribute. It uses the 'check_password_hash' function from
        the Flask-Bcrypt library to perform the verification.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """

        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Function that converts the user object to a dictionary

        This function converts the user object to a dictionary representation, with the user's
        'id', 'email', 'is_active' and 'is_authenticated' attributes as keys.

        Returns:
            dict: a dictionary representation of the user object.
        """

        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'is_authenticated': self.is_authenticated
        }


class Coin(db.Model):  # pylint: disable=too-few-public-methods
    """
    Defines a SQLAlchemy model for a cryptocurrency.

    This model defines a cryptocurrency with an index and abbreviation. It also
    includes a relationship with the `Balance` model.

    Attributes:
        id (int): The primary key for the cryptocurrency.
        index (str): The index of the cryptocurrency.
        abbreviation (str): The abbreviation of the cryptocurrency.

    Relationships:
        balances (One-to-Many): Defines a one-to-many relationship between the `Coin`
        model and the `Balance` model. This relationship allows a cryptocurrency to
        have multiple balance objects associated with it.

    """

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(30), nullable=False)
    abbreviation = db.Column(db.String(30))

    balances = db.relationship('Balance', backref='coin')

    def to_dict(self):
        """
        Function that converts the coin object to a dictionary

        This function converts the user object to a dictionary representation, with the coin's
        'id' and 'abbreviation' attributes as keys.

        Returns:
            dict: a dictionary representation of the coin object.
        """

        return {
            'id': self.id,
            'abbreviation': self.abbreviation,
        }


class Balance(db.Model):  # pylint: disable=too-few-public-methods
    """
    Defines a SQLAlchemy model for a user balance.

    This model defines a user balance with an amount and date added. It also
    includes foreign keys to the `User` and `Coin` models.

    Attributes:
        id (int): The primary key for the user balance.
        amount (decimal): The amount of the associated coin in the user's account.
        date_added (datetime): The date and time when the user balance was added.

    Foreign Keys:
        user_id (int): A foreign key to the `User` model, indicating which user account
        the balance is associated with.
        coin_id (int): A foreign key to the `Coin` model, indicating which coin the balance
        is associated with.

    """

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL(15, 7))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'))

    def to_dict(self):
        """
        Function that converts the balance object to a dictionary

        This function converts the balance object to a dictionary representation, with the balance's
        'id', 'user', 'coin' and 'amount' attributes as keys.

        Returns:
            dict: a dictionary representation of the balance object.
        """
        # amount = "{:.7f}".format(self.amount).rstrip('0')
        amount = f"{self.amount:.7f}".rstrip('0')
        return {
            'id': self.id,
            'user': self.user_id,
            'coin': self.coin.abbreviation,
            'amount': amount.rstrip('.') if amount.endswith('.') else amount,
        }
