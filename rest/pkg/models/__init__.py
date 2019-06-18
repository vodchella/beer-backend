from datetime import datetime
from peewee import *
from pkg.app import app
from pkg.constants.database import ID_FIELD_LENGTH


class User(app.db.AsyncModel):
    user_id = FixedCharField(max_length=ID_FIELD_LENGTH, primary_key=True)
    email = TextField()
    password = TextField()
    active_bool = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        schema = 'public'
        db_table = 'users'
