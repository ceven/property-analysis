from typing import Optional

from firebase_admin import auth
from firebase_admin.auth import UserRecord

# Implement auth with python and firebase: https://medium.com/the-infinite-machine/truly-authul-41cc570da172
from requests import HTTPError

from firebasedb import pyrebase_app, pyrebase_auth


def get_user(user_email: str) -> Optional[UserRecord]:
    try:
        return auth.get_user_by_email(user_email)
    except auth.AuthError:
        return None


def register_user(user_email: str, user_password: str):
    auth.create_user(email=user_email, password=user_password)


def login_user(user_email: str, user_password: str) -> Optional[UserRecord]:
    try:
        user = pyrebase_auth.sign_in_with_email_and_password(user_email, user_password)
    except HTTPError as e:
        print(e)  # FIXME remove
        user = None
    return user
