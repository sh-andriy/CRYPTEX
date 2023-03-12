from dataclasses import dataclass
import requests

from flask_login import LoginManager


login_manager = LoginManager()


@dataclass
class CustomUser:
    """
    A class that represents a custom user object.

    Attributes:
    id(str): The ID of the user;
    email(str): The email address of the user;
    is_active(bool): A boolean indicating whether the user is active;
    is_authenticated(bool): A boolean indicating whether the user is authenticated;
    url(str): The URL of the user's API endpoint.

    """
    id: str  # pylint: disable=C0103
    email: str
    is_active: bool
    is_authenticated: bool
    url: str

    def get_id(self):
        """
        Function that gets id of the user

        Returns:
            str: The id of a user
        """
        return self.url

    @classmethod
    def create_from_api(
        cls,
        url: str
    ):
        """
        Function that creates a custom user object from an API response

        Args:
            url(str): the url of the user's API endpoint.

        Returns:
            CustomUser: a custom user object.
        """
        response = requests.get(url=url, timeout=5).json()['user']
        user = cls(
            id=response['id'],
            email=response['email'],
            is_active=response['is_active'],
            is_authenticated=response['is_authenticated'],
            url=url
        )
        return user
