import re

from sqlalchemy import text, exc

from .exception import SqlAlchemyException
from .util import classproperty, get_column_attr, get_type, get_count, QUERY_MATCHES
from .session_mixin import SessionMixin
from .inspection_mixin import InspectionMixin


class CrudMixin(InspectionMixin, SessionMixin):
    __abstract__ = True

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def filter(cls, *arg):
        return cls.query.filter(*arg).order_by(None)

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
        return self

    def save(self):
        """Saves the updated model to the current entity db.
        """
        try:
            self.session.add(self)
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            if isinstance(e, exc.IntegrityError):
                message = e.args[0].split('=')[1].replace('(', '').replace(')', '').rstrip()
                raise SqlAlchemyException(message)
            raise SqlAlchemyException(e.__str__())
        else:
            return self

    @classmethod
    def create(cls, **kwargs):
        """Create and persist a new record for the model
        :param kwargs: attributes for the record
        :return: the new model instance
        """
        return cls(**kwargs).save()

    def update(self, **kwargs):
        """Same as :meth:`fill` method but persists changes to database.
        """
        return self.fill(**kwargs).save()

    def delete(self):
        """Removes the model from the current entity session and mark for deletion.
        """
        self.session.delete(self)
        self.session.flush()

    @classmethod
    def destroy(cls, *ids):
        """Delete the records with the given ids
        :type ids: list
        :param ids: primary key ids of records
        """
        for pk in ids:
            obj = cls.find(pk)
            if obj:
                obj.delete()
        cls.session.flush()

    @classmethod
    def get(cls, id_):
        """Find record by the id
        :param id_: the primary key
        """
        return cls.query.get(id_)

    @classmethod
    def get_or_abort(cls, id_):
        r = cls.get(id_)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SqlAlchemyException(message)
        return r

    @classmethod
    def find(cls, *arg):
        return cls.filter(*arg).order_by(None).limit(1).first()

    @classmethod
    def find_or_abort(cls, *arg):
        r = cls.find(*arg)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SqlAlchemyException(message)
        return r

    @classmethod
    def find_one(cls, **kwargs):
        return cls.filter_by(**kwargs).order_by(None).limit(1).first()

    @classmethod
    def find_one_or_abort(cls, **kwargs):
        r = cls.find_one(**kwargs)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SqlAlchemyException(message)
        return r

    @classmethod
    def check_and_abort(cls, *arg):
        if cls.find(*arg) is not None:
            message = "Record '{}' exist".format(cls.__table__.name)
            raise SqlAlchemyException(message)
        return True

    @classmethod
    def find_or_create(cls, **kwargs):
        if kwargs is None:
            return None
        obj = cls.find_one(**kwargs)
        if obj is not None:
            return obj
        obj = cls.create(**kwargs)
        return obj

    @classmethod
    def handle_query(cls, **data):
        if 'query' in data and data['query'] is not None:
            return data.get('query')
        return cls.filter()

    @classmethod
    def filter_with_args(cls, **data):
        query = cls.handle_query(**data)
        if 'filter' in data and data['filter'] is not None and bool(data['filter']):
            for key, value in data.get('filter').items():
                column = get_column_attr(cls, key)
                if column is not None and len(str(value)) > 0 and value is not None:
                    column_type = get_type(column)
                    column_type = re.sub('[^A-Za-z]+', '', str(column_type))
                    if isinstance(value, list):
                        column_type = 'LIST'
                    query = QUERY_MATCHES[column_type](query, column, value)

        order_by = data['sortField'] + " " + data['sortOrder']
        query = query.order_by(text(order_by))
        if data['pageNumber'] == 0 and data['pageSize'] == 0:
            return get_count(query), query
        return query.paginate(data['pageNumber'], data['pageSize'])
