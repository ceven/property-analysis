from django.contrib import auth


def logout_user(request) -> None:
    try:
        auth.logout(request)
    except KeyError as e:
        print(e)  # FIXME remove
