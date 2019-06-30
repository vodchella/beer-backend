from playhouse.postgres_ext import BinaryJSONField
from pkg.rest import app
from pkg.models.fields import *


class User(app.db.AsyncModel):
    user_id = PrimaryKeyCharField()
    email = TextField()
    password = TextField()
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        db_table = 'users'


class Company(app.db.AsyncModel):
    company_id = PrimaryKeyCharField()
    name = TextField()
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        db_table = 'companies'


class ServicePoint(app.db.AsyncModel):
    service_point_id = PrimaryKeyCharField()
    name = TextField()
    company_id = ForeignKeyCharField(Company)
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        db_table = 'service_points'


class Employee(app.db.AsyncModel):
    employee_id = PrimaryKeyCharField()
    user_id = ForeignKeyCharField(User)
    service_point_id = ForeignKeyCharField(ServicePoint)
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        db_table = 'employees'


class Card(app.db.AsyncModel):
    card_id = PrimaryKeyCharField()
    card_number = CharField(max_length=20)
    type_of_card = CharField(max_length=15)
    attributes = BinaryJSONField()
    company_id = ForeignKeyCharField(Company)
    owner_id = ForeignKeyCharField(User)
    issuer_id = ForeignKeyCharField(Employee)
    issued_in_service_point_id = ForeignKeyCharField(ServicePoint)
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        db_table = 'cards'
