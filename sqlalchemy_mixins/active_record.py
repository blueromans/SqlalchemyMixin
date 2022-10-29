import sqlalchemy as sa
from slugify import slugify

from .crud_mixin import CrudMixin


class ActiveRecordMixin(CrudMixin):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    active = sa.Column(sa.Boolean, nullable=False, server_default='1')

    def __init__(self, *args, **kwargs):
        if 'slug' in self.settable_attributes:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    def toggle_status(self):
        self.active = not self.active
        self.save()
