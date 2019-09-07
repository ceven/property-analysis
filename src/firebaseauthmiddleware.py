import functools
from typing import Optional, Any

from django.shortcuts import redirect
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from requests import HTTPError

from firebasedb import pyrebase_auth


def get_user(user_email: str) -> Optional[UserRecord]:
    try:
        return auth.get_user_by_email(user_email)
    except auth.AuthError:
        return None


def check_authenticated(function):
    @functools.wraps(function)
    def wrapper(request, *args, **kwargs):
        sess = request.session
        ok = False
        if sess and 'token' in sess and 'local_id' in sess:
            try:
                decoded_token = auth.verify_id_token(id_token=sess['token'], check_revoked=True)
                uid = decoded_token['uid']
                ok = (uid == sess['local_id'])
            except Exception as e:
                print(e)
        if not ok:
            return redirect_login_view()
        return function(request, *args, **kwargs)
    return wrapper


def redirect_login_view():
    return redirect('/property/login')


def check_authorised():
    return True  # FIXME authorisation to access resources ; user id should prefix resource!


def register_user(user_email: str, user_password: str) -> UserRecord:
    return auth.create_user(email=user_email, password=user_password)


def login_user(user_email: str, user_password: str) -> Any:
    try:
        json_resp = pyrebase_auth.sign_in_with_email_and_password(user_email, user_password)
    except HTTPError as e:
        json_resp = None
    return json_resp
