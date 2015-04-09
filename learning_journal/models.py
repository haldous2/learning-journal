from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

## It should be stored in a database table called entries
## It should have a primary key field called id
## It should have a title field which accepts unicode text up to 255 characters in length
## -- maybe... The title should be unique and it should be impossible to save an entry without a title.
## -- need to test... It should have a body field which accepts unicode text of any length (including none)
## It should have a created field which stores the date and time the object was created.
## It should have an edited field which stores the date and time the object was last edited.
## Both the created and edited field should default to now if not provided when a new instance is constructed.
#The entry class should support a classmethod all that returns all the entries in the database, ordered so that the most recent entry is first.
#The entry class should support a classmethod by_id that returns a single entry, given an id.

class Entries(Base):

    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    body = Column(Text)
    created = Column(Date, default=_get_date)
    edited = Column(Date, default=_get_date, onupdate=_get_date)

    @title.setter
    def title(self, value):
        if (value == ""):
            raise Exception
        else
            title = value
