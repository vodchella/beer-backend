from datetime import datetime
from peewee import *
from pkg.app import app
from pkg.constants.database import ID_FIELD_LENGTH


class PrimaryKeyCharField(FixedCharField):
    def __init__(self, *args):
        super(FixedCharField, self).__init__(*args, max_length=ID_FIELD_LENGTH, primary_key=True)


class IsActiveField(BooleanField):
    def __init__(self, *args):
        super(BooleanField, self).__init__(*args, default=True, db_column='active_bool')


class CreatedAtField(DateTimeField):
    def __init__(self, *args):
        super(DateTimeField, self).__init__(*args, default=datetime.now)


#
#  Сущности базы данных
#


class User(app.db.AsyncModel):
    user_id = PrimaryKeyCharField()
    email = TextField()
    password = TextField()
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        schema = 'public'
        db_table = 'users'


class Company(app.db.AsyncModel):
    company_id = PrimaryKeyCharField()
    name = TextField()
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        schema = 'public'
        db_table = 'companies'


class ServicePoint(app.db.AsyncModel):
    service_point_id = PrimaryKeyCharField()
    name = TextField()
    company = ForeignKeyField(Company)
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        schema = 'public'
        db_table = 'service_points'
