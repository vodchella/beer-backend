import jwt
from datetime import datetime, timedelta
from pkg.models import User


def _create_token(user: User, secret: str, token_type: str):
    if token_type == 'a':
        expires_at = datetime.utcnow() + timedelta(hours=2)
    elif token_type == 'r':
        expires_at = datetime.utcnow() + timedelta(days=7)
    else:
        raise Exception('Invalid token type')

    payload = {
        'ver': 1,
        'uid': user.user_id,
        'exp': expires_at,
        'typ': token_type
    }

    return jwt.encode(payload, secret, algorithm='HS256')


def create_auth_token(user: User, secret: str):
    return _create_token(user, secret, 'a')


def create_refresh_token(user: User, secret: str):
    return _create_token(user, secret, 'r')


def create_secret(user: User, token_key: str = None):
    key = token_key if token_key else user.token_key
    return f'{user.password}-{user.user_id}-{key}'
