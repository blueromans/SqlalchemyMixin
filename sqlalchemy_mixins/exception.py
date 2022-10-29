class ImproperlyConfigured(Exception):
    """
    SQLAlchemy-Utils is improperly configured; normally due to usage of
    a utility that depends on a missing library.
    """


class SqlAlchemyException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
