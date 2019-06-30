import jwt
from datetime import datetime


def create_token(user, token_type):
    if token_type not in ['a', 'r']:
        raise Exception('Invalid token type')

    key = f'{user.password}-{user.user_id}'
    payload = {
        'uid': user.user_id,
        'exp': datetime.utcnow(),
        'typ': token_type
    }

    return jwt.encode(payload, key, algorithm='HS256')
