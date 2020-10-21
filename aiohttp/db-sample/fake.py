from faker import Faker
from sqlalchemy.exc import IntegrityError

from models import (
    User,
    Role
)

def users(session, count=100, seed=1651):
    """
    If database has some users, it is likely that we renerate a user with 
    the same name
    
    InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Originalexception was: (psycopg2.IntegrityError) duplicate key value violates unique constraint "ix_users_username"
    DETAIL:  Key (username)=(mtaylor) already exists.
    """
    fake = Faker('en_US')
    fake.seed(seed)

    i=0
    while i<count:
        u = User(email=fake.email(),
            name=fake.user_name(),
            fullname=fake.name(),
            password_hash='password',
            confirmed=True,
            member_since=fake.past_date(),
            last_seen=fake.past_date())

        u.role = session.query(Role).filter_by(default=True).first()

        # At this point, we say that the instance is pending; 
        # no SQL has yet been issued and the object is not yet represented 
        # by a row in the database

        # Session will issue the sql to persist this user as soon as is needed
        # using a process known as a flush!
        session.add(u)

        try:
            session.commit()
            i+=1
        except IntegrityError:
            session.rollback()