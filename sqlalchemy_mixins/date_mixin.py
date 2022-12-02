import os
from datetime import datetime

import arrow
import sqlalchemy as sa


class DateMixin:
    """Mixin that define timestamp columns."""

    __abstract__ = True

    __created_at_name__ = 'created_at'
    __updated_at_name__ = 'updated_at'
    __datetime_func__ = datetime.now()

    created_at = sa.Column(__created_at_name__,
                           sa.TIMESTAMP(timezone=False),
                           default=__datetime_func__,
                           nullable=False)

    updated_at = sa.Column(__updated_at_name__,
                           sa.TIMESTAMP(timezone=False),
                           default=__datetime_func__,
                           onupdate=__datetime_func__,
                           nullable=False)

    @property
    def is_new(self):
        if self.created_at is not None:
            timedelta = round(
                (datetime.now() - self.created_at).total_seconds() / 60)
            return timedelta <= os.environ.get('IS_NEW_TIME_INTERVAL', 120)
        return False

    def create_date(self, tzinfo='Europe/Istanbul', locale='tr_tr', format='DD MMMM YYYY dddd HH:mm'):
        if self.created_at is not None:
            timedelta = round((datetime.now() - self.created_at).days)
            if timedelta < 2:
                return arrow.get(self.created_at.isoformat(), tzinfo=tzinfo).humanize(locale=locale).title()
            return arrow.get(self.created_at.isoformat(), tzinfo=tzinfo).format(format, locale=locale)
        return ' --- '

    def update_date(self, tzinfo='Europe/Istanbul', locale='tr_tr', format='DD MMMM YYYY dddd HH:mm'):
        if self.updated_at is not None:
            timedelta = round((datetime.now() - self.created_at).days)
            if timedelta < 2:
                return arrow.get(self.updated_at.isoformat(), tzinfo=tzinfo).humanize(locale=locale).title()
            return arrow.get(self.updated_at.isoformat(), tzinfo=tzinfo).format(format, locale=locale)
        return ' --- '
