from pkg.models import User
from pkg.rest import app
from pkg.utils.argon import *


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
