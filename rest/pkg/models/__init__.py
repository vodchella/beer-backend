from datetime import datetime
from peewee import *
from pkg.app import app
from pkg.constants.database import ID_FIELD_LENGTH


class PrimaryKeyCharField(FixedCharField):
    def __init__(self, *args):
        super(FixedCharField, self).__init__(*args, max_length=ID_FIELD_LENGTH, primary_key=True)


class ForeignKeyCharField(FixedCharField):
    def __init__(self, rel_model, related_name=None, on_delete=None,
                 on_update=None, extra=None, to_field=None,
                 object_id_name=None, *args, **kwargs):
        if rel_model != 'self' and not \
                isinstance(rel_model, (Proxy, DeferredRelation)) and not \
                issubclass(rel_model, Model):
            raise TypeError('Unexpected value for `rel_model`.  Expected '
                            '`Model`, `Proxy`, `DeferredRelation`, or "self"')
        self.rel_model = rel_model
        self._related_name = related_name
        self.deferred = isinstance(rel_model, (Proxy, DeferredRelation))
        self.on_delete = on_delete
        self.on_update = on_update
        self.extra = extra
        self.to_field = to_field
        self.object_id_name = object_id_name
        super(ForeignKeyCharField, self).__init__(*args, max_length=ID_FIELD_LENGTH, **kwargs)


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
    company_id = ForeignKeyCharField(Company)
    is_active = IsActiveField()
    created_at = CreatedAtField()

    class Meta:
        schema = 'public'
        db_table = 'service_points'
