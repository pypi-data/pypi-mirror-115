from typing import Dict, Any
from sqlalchemy import orm, engine
from functools import cached_property


class SqlEngine(object):

    Session = orm.Session

    def __init__(self, uri: str, pool_size: int = 1):
        self.uri = uri
        self.pool_size = pool_size

    @property
    def settings(self) -> Dict[str, Any]:
        return {
            'echo': False,
            'pool_pre_ping': True,
            'pool_size': self.pool_size,
        }

    @cached_property
    def engine(self) -> engine.Engine:
        return engine.create_engine(self.uri, **self.settings)

    @cached_property
    def session(self) -> orm.scoped_session:
        orm.configure_mappers()
        factory = orm.sessionmaker(bind=self.engine, expire_on_commit=False)
        session_class = orm.scoped_session(factory)
        return session_class

    @cached_property
    def registry(self) -> orm.registry:
        return orm.registry()

    def make_session(self, *args, **kwargs):
        """
        Create a new database session.

        :rtype: sqlalchemy.orm.Session
        """
        return self.session(*args, **kwargs)

    def inject_session(self, func):
        """
        Function decorator which injects a "session" named parameter
        if it doesn't already exists
        """
        def session_wrapper(*args, **kwargs):
            session = kwargs.setdefault('session', self.make_session())
            try:
                return func(*args, **kwargs)
            finally:
                session.close()

        return session_wrapper

    def atomic(self, func):
        """
        Function decorator which injects a "session" named parameter
        if it doesn't already exists, and wraps the function in an
        atomic transaction.
        """
        @self.inject_session
        def atomic_wrapper(*args, **kwargs):
            session: orm.Session = kwargs['session']
            session.begin()

            try:
                return_value = func(*args, **kwargs)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                return return_value

        return atomic_wrapper
