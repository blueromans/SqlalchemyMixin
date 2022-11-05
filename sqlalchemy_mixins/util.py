from sqlalchemy import func, String
from sqlalchemy.orm import InstrumentedAttribute, ColumnProperty, RelationshipProperty

QUERY_MATCHES = {'BOOLEAN': (lambda query, column, value: query.filter(column == bool(int(value)))),
                 'VARCHAR': (lambda query, column, value: query.filter(
                     func.lower(func.cast(column,String)).contains("%" + value.lower() + "%"))),
                 'INTEGER': (lambda query, column, value: query.filter(column == int(value))),
                 'LIST': (lambda query, column, value: query.filter(column.in_(value))),
                 }


def str_coercible(cls):
    def __str__(self):
        return self.__unicode__()

    cls.__str__ = __str__
    return cls


class ScalarCoercible:
    def _coerce(self, value):
        raise NotImplementedError

    def coercion_listener(self, target, value, oldvalue, initiator):
        return self._coerce(value)


class classproperty(object):
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def get_column_attr(object_cls, key):
    try:
        return getattr(object_cls, key)
    except:
        return None


def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count


def get_type(expr):
    """
    Return the associated type with given Column, InstrumentedAttribute,
    ColumnProperty, RelationshipProperty or other similar SQLAlchemy construct.

    For constructs wrapping columns this is the column type. For relationships
    this function returns the relationship mapper class.

    :param expr:
        SQLAlchemy Column, InstrumentedAttribute, ColumnProperty or other
        similar SA construct.

    ::

        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String)


        class Article(Base):
            __tablename__ = 'article'
            id = sa.Column(sa.Integer, primary_key=True)
            author_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
            author = sa.orm.relationship(User)


        get_type(User.__table__.c.name)  # sa.String()
        get_type(User.name)  # sa.String()
        get_type(User.name.property)  # sa.String()

        get_type(Article.author)  # User


    .. versionadded: 0.30.9
    """
    if hasattr(expr, 'type'):
        return expr.type
    elif isinstance(expr, InstrumentedAttribute):
        expr = expr.property

    if isinstance(expr, ColumnProperty):
        return expr.columns[0].type
    elif isinstance(expr, RelationshipProperty):
        return expr.mapper.class_
    raise TypeError("Couldn't inspect type.")
