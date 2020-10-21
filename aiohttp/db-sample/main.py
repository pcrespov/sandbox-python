"""

Exerciseing http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""

import logging

import sqlalchemy
from sqlalchemy import create_engine

logging.basicConfig(level=logging.DEBUG)

_LOGGER = logging.getLogger()

_LOGGER.debug("sqlalchemy %s", sqlalchemy.__version__)

config = dict(user='su', password='secret', hostname='localhost', dbname='db')

#URL+  dialect[+driver]://user:password@host/dbname[?key=value..]
URL = "postgresql+psycopg2://{user}:{password}@{hostname}/{dbname}"

#engine = create_engine("sqlite:///:memory:", echo=True)
engine = create_engine(URL.format(**config), echo=True)

# The ORM’s “handle” to the database is the Session. When we first set up the application, 
# at the same level as our create_engine() statement, we define a Session class which 
# will serve as a factory for new Session objects

# TODO: one engine per thread and a session per project-session?
from sqlalchemy.orm import sessionmaker
DbSession = sessionmaker(bind=engine)


# Then, whenever you need to have a conversation with the database
session = DbSession()

# session.new
# session.dirty
# 

from models import (
    Base, 
    User,
    Role
)


# init
Base.metadata.create_all(engine)
Role.add_roles(session)


#import fake
#fake.users(session, 3)
#ed_user = User(name='pcrespov', fullname='pcrespov', email='pcrespo@d.com')
#session.query(User).filter_by(email='asmith@li.com').all()
