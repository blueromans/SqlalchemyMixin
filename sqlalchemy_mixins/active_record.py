import sqlalchemy as sa

from .crud_mixin import CrudMixin


class ActiveRecordMixin(CrudMixin):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    active = sa.Column(sa.Boolean, nullable=False, server_default='1')

    def toggle_status(self):
        self.active = not self.active
        self.save()
