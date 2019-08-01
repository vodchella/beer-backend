from datetime import datetime
from peewee import *
from pkg.constants.database import ID_FIELD_LENGTH


class PrimaryKeyCharField(FixedCharField):
    def __init__(self, *args):
        super(FixedCharField, self).__init__(*args, max_length=ID_FIELD_LENGTH, primary_key=True)


class ForeignKeyCharField(FixedCharField):
    def __init__(self, rel_model, *args, **kwargs):
        if rel_model != 'self' and not \
                isinstance(rel_model, (Proxy, DeferredRelation)) and not \
                issubclass(rel_model, Model):
            raise TypeError('Unexpected value for `rel_model`.  Expected '
                            '`Model`, `Proxy`, `DeferredRelation`, or "self"')
        self.rel_model = rel_model
        self._related_name = kwargs.get('related_name', None)
        self.deferred = isinstance(rel_model, (Proxy, DeferredRelation))
        self.on_delete = kwargs.get('on_delete', None)
        self.on_update = kwargs.get('on_update', None)
        self.extra = kwargs.get('extra', None)
        self.to_field = kwargs.get('to_field', None)
        self.object_id_name = kwargs.get('object_id_name', None)
        super(ForeignKeyCharField, self).__init__(*args, max_length=ID_FIELD_LENGTH, **kwargs)


class IsActiveField(BooleanField):
    def __init__(self, *args):
        super(BooleanField, self).__init__(*args, default=True, db_column='active_bool')


class CreatedAtField(DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.pop('default', None)
        super(DateTimeField, self).__init__(*args, **kwargs, default=datetime.now)
