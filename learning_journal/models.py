import datetime

from sqlalchemy import (
    and_,
    Column,
    DateTime,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    )

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
from cryptacular.bcrypt import BCRYPTPasswordManager

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

##
# Add entries to Entry
#
# initialize_learning_journal_db development.ini (run to create table - if this hasn't been done yet...)
#
# >>> from ljshell import Session
# >>> from learning_journal.models import Entry
# >>> session = Session()
#
# >>> new_model = Entry(title='the title', body='the body')
# >>> session.add(new_model)
#
# OR
#
# >>> session.add(Entry(title='blog post one', body='this is the body of blog post one'))
# >>> session.add(Entry(title='blog post two', body='this is the body of blog post two'))
# >>> session.add(Entry(title='blog post three', body='this is the body of blog post three'))
# >>> session.add(Entry(title='blog post four', body='this is the body of blog post four'))
#
# >>> session.commit()
#
# >>> session.query(Entry).count() (quick test to see how many records are in in the table)
##

class Entry(Base):

    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        """return a query with all entries, ordered by creation date reversed
        """
        if session is None:
            session = DBSession
        return session.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id, session=None):
        """return a single entry identified by id
        If no entry exists with the provided id, return None
        """
        if session is None:
            session = DBSession
        return session.query(cls).get(id)

##
#
# Security basics:
#   who you are   - facial biometric, fingerprints
#   what you have - your phone, key generator
#   what you know - your password - keylogger can steal this
#
#   Notes: 1. never store passwords in plain text, always hash and query by hash
#          2. always use two factor authentication
#          3. users should have authentication roles (policies)
#          4. always look up user + password, not by single entities in order to thwart hackers
#
##
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    hashword = Column(Unicode(255), nullable=False)

    ##
    # Note: it appears that classes and attributes can be added, updated on the fly
    ##

    @classmethod
    def by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()

    def verify_password(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.hashword, password)

    @classmethod
    def by_name_and_hash(cls, name, hashword):
        return DBSession.query(cls).filter(cls.name == name, cls.hashword == hashword).first()
        #return DBSession.query(cls).filter(and_(cls.name == name, cls.hashword == hashword)).first()

    @classmethod
    def by_name_and_password(cls, name, password):
        manager = BCRYPTPasswordManager()
        return User.by_name_and_hash(name, manager.encode(password))
