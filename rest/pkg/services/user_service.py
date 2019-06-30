from pkg.models import User
from pkg.rest import app
from pkg.utils.argon import *
from pkg.utils.jwt import *
from pkg.utils.peewee import generate_unique_id


class UserService:
    @staticmethod
    async def find(user_id):
        try:
            return await app.db.aio.get(User, User.user_id == user_id)
        except:
            return None

    @staticmethod
    def verify_password(user, password):
        try:
            return verify_hash(user.password, password)
        except:
            return False

    @staticmethod
    async def set_password(user, new_password):
        user.password = hash_password(new_password)
        await app.db.aio.update(user)

    @staticmethod
    async def create_new_tokens(user):
        new_token_key = generate_unique_id()
        user.token_key = new_token_key
        await app.db.aio.update(user)

        key = f'{user.password}-{user.user_id}-{new_token_key}'

        auth_token = create_auth_token(user, key)
        refresh_token = create_refresh_token(user, key)
        return {'auth': auth_token, 'refresh': refresh_token}
