from .active_record import ActiveRecordMixin
from .date_mixin import DateMixin
from .image_mixin import ImageMixin
from .smart_query import SmartQueryMixin
from .repr_mixin import ReprMixin
from .user_mixin import UserMixin
from .crud_mixin import CrudMixin
from .base_query import BaseQuery
from .exception import SqlAlchemyException
from .extra import PhoneNumber


class BaseMixin(ActiveRecordMixin, DateMixin, SmartQueryMixin, ReprMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__
