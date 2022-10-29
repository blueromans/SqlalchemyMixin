from sqlalchemy import orm


class BaseQuery(orm.Query):

    def paginate(self, page, per_page):
        return self.count(), self.limit(per_page).offset((page - 1) * per_page)
