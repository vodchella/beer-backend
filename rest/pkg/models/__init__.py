from datetime import datetime
from peewee import *
from pkg.app import app


class User(app.db.AsyncModel):
    user_id = FixedCharField(max_length=16, primary_key=True)
    email = TextField()
    password = TextField()
    seller_bool = BooleanField(default=False)
    active_bool = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        schema = 'public'
        db_table = 'users'
