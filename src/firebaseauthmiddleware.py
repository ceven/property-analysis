from typing import Optional, Any

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


def check_authenticated(session) -> bool:
    if not session or 'token' not in session:
        return False
    try:
        check = auth.verify_id_token(id_token=session['token'], check_revoked=True)
        return True
    except Exception as e:
        print(e)
        return False


def check_authorised():
    return True  # FIXME authorisation to access resources ; user id should prefix resource!


def register_user(user_email: str, user_password: str):
    auth.create_user(email=user_email, password=user_password)


def login_user(user_email: str, user_password: str) -> Any:
    try:
        json_resp = pyrebase_auth.sign_in_with_email_and_password(user_email, user_password)
    except HTTPError as e:
        print(e)  # FIXME remove
        json_resp = None
    return json_resp
