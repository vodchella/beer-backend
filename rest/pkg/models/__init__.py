from datetime import datetime
from peewee import *
from pkg.app import app
from pkg.constants.database import ID_FIELD_LENGTH


class User(app.db.AsyncModel):
    user_id = FixedCharField(max_length=ID_FIELD_LENGTH, primary_key=True)
    email = TextField()
    password = TextField()
    is_active = BooleanField(default=True, db_column='active_bool')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        schema = 'public'
        db_table = 'users'


class Company(app.db.AsyncModel):
    company_id = FixedCharField(max_length=ID_FIELD_LENGTH, primary_key=True)
    name = TextField()
    is_active = BooleanField(default=True, db_column='active_bool')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        schema = 'public'
        db_table = 'companies'
