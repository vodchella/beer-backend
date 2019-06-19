from pkg.app import app
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
