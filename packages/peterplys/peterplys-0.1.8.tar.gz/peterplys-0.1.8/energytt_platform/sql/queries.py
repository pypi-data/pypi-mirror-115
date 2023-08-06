

class SqlQuery(object):
    """
    TODO
    """
    def __init__(self, session, q):
        """
        :param sqlalchemy.orm.Session session:
        :param sqlalchemy.orm.Query q:
        """
        self.session = session
        self.q = q

    def __iter__(self):
        return iter(self.q)

    def __getattr__(self, name):
        return getattr(self.q, name)

    def filter(self, *filters):
        return self.__class__(self.session, self.q.filter(*filters))

    def unique_join(self, *props, **kwargs):
        if props[0] in [c.entity for c in self.q._join_entities]:
            return self

        return self.__class__(self.session, self.q.join(
            *props, **kwargs
        ))

    def lazy_load(self, field):
        return self.__class__(self.session, self.q.options(
            lazyload(field)
        ))

    def eager_load(self, path, *fields):
        if isinstance(path, (list, tuple)):
            join = joinedload(*path)
        else:
            join = joinedload(path)

        if fields:
            join = join.load_only(*fields)
        return self.__class__(self.session, self.q.options(
            join
        ))

    # def eage_load_path(self, *path):
    #     join = rjoinedload(*path)
    #     if fields:
    #         join = join.load_only(*fields)
    #     return self.__class__(self.session, self.q.options(
    #         join
    #     ))

    def only(self, *fields):
        return self.__class__(self.session, self.q.options(
            load_only(*fields)
        ))

    def get(self, field):
        return self.only(field).scalar()

    def exists(self):
        return self.count() > 0
