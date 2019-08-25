from typing import Optional

from firebase_admin import auth
from firebase_admin.auth import UserRecord


def get_user(user_email: str) -> Optional[UserRecord]:
    try:
        return auth.get_user_by_email(user_email)
    except auth.AuthError:
        return None


def register_user(user_email: str, user_password: str):
    auth.create_user(email=user_email, password=user_password)
