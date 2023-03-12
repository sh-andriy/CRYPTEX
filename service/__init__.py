from dataclasses import dataclass
import requests

from flask_login import LoginManager


login_manager = LoginManager()


@dataclass
class CustomUser:
    id: str
    email: str
    is_active: bool
    is_authenticated: bool
    url: str

    def get_id(self):
        return self.url

    @classmethod
    def create_from_api(
        cls,
        url: str
    ):
        response = requests.get(url=url).json()['user']
        user = cls(
            id=response['id'],
            email=response['email'],
            is_active=response['is_active'],
            is_authenticated=response['is_authenticated'],
            url=url
        )
        return user

