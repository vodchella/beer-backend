from pkg.models import User
from pkg.utils.argon import *
from pkg.utils.context import get_current_context
from pkg.utils.jwt import *
from pkg.utils.peewee import generate_unique_id


class UserService:
    @staticmethod
    async def find(user_id):
        ctx = get_current_context()
        try:
            return await ctx.db.get(User, User.user_id == user_id)
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
        ctx = get_current_context()
        user.password = hash_password(new_password)
        await ctx.db.update(user)

    @staticmethod
    async def create_new_tokens(user):
        ctx = get_current_context()

        new_token_key = generate_unique_id()
        user.token_key = new_token_key
        await ctx.db.update(user)

        secret = create_secret(user)

        auth_token = create_auth_token(user, secret)
        refresh_token = create_refresh_token(user, secret)
        return {'auth': auth_token, 'refresh': refresh_token}
