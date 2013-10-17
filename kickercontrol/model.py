from hashlib import sha1
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import UserMixin
from .hash_passwords import check_hash, make_hash
from .auth import login_serializer

db_engine = None
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))


def init_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri)
    db_session.configure(bind=db_engine)


def init_db():
    Base.metadata.create_all(bind=db_engine)


def clear_db():
    Base.metadata.drop_all(bind=db_engine)


class Base(object):
    id = Column(Integer, primary_key=True)


class HasUniqueName(object):
    name = Column(Text, nullable=False, unique=True)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.name)


Base = declarative_base(cls=Base)
Base.query = db_session.query_property()


class User(UserMixin, Base):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=False)
    email = Column(Text, nullable=False, unique=True)
    _password = Column('password', Text, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def get_auth_token(self):
        data = (self.id, sha1(self.password).hexdigest())
        return login_serializer.dumps(data)

    def _set_password(self, password):
        self._password = make_hash(password)

    def _get_password(self):
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def valid_password(self, password):
        """Check if provided password is valid."""
        return check_hash(password, self.password)

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id,
                                 self.username)


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    teamBlack_result = Column(Integer, default=0)
    teamRed_result = Column(Integer, default=0)
    
    teamBlack_frontend = Column(Integer, ForeignKey('users.id'))
    teamBlack_backend = Column(Integer, ForeignKey('users.id'))
    teamRed_frontend = Column(Integer, ForeignKey('users.id'))
    teamRed_backend = Column(Integer, ForeignKey('users.id'))

    teamBlack_frontend_rel = relationship("User", foreign_keys="[User.id]", primaryjoin="User.id==Game.teamBlack_frontend")
    teamBlack_backend_rel = relationship("User", foreign_keys="[User.id]", primaryjoin="User.id==Game.teamBlack_backend")
    teamRed_frontend_rel = relationship("User", foreign_keys="[User.id]", primaryjoin="User.id==Game.teamRed_frontend")
    teamRed_backend_rel = relationship("User", foreign_keys="[User.id]", primaryjoin="User.id==Game.teamRed_backend")
