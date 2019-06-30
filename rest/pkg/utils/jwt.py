import jwt
from datetime import datetime


def _create_token(user, key, token_type):
    if token_type not in ['a', 'r']:
        raise Exception('Invalid token type')

    payload = {
        'uid': user.user_id,
        'exp': datetime.utcnow(),
        'typ': token_type
    }

    return jwt.encode(payload, key, algorithm='HS256')


def create_auth_token(user, key):
    return _create_token(user, key, 'a')


def create_refresh_token(user, key):
    return _create_token(user, key, 'r')
