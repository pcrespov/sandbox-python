from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text,
    ForeignKey
)    
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

def mixin_todict(self):
    dikt = dict()
    for key in self.__table__.columns.keys():
       dikt[key] = getattr(self, key)
    return dikt

def create_gravatar_hash(email):
    import hashlib
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

#-------------------------------------------------------------------

class Permission:
    READ = 1
    WRITE = 2
    MODERATE = 4
    ADMIN = 16 # Super-user


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    default = Column(Boolean, default=False, index=True)
    permissions = Column(Integer)

    users = relationship('User', back_populates='role', lazy='dynamic') # 

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def add_roles(session):
        """
            Definition of roles
        """
        roles = {
            'User': [
                Permission.READ, 
                Permission.WRITE
                ],
            'Administrator': [
                Permission.WRITE, 
                Permission.MODERATE,
                Permission.ADMIN
                ],
            }
        default_role = 'User'
        #-
        for r in roles.keys():
            role = session.query(Role).filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            session.add(role)
        session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name



#--------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String)    
    password_hash = Column(String)
    member_since = Column(DateTime(), default=datetime.utcnow)    
    avatar_hash = Column(String)
    # relations
    role_id = Column(Integer, ForeignKey("roles.id"))   # constrained to values in roles.id
    role = relationship("Role", back_populates="users") # 
    
    # admin
    confirmed = Column(Boolean, default=False)
    last_seen = Column(DateTime(), default=datetime.utcnow)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        #if self.role is None:
        #    self.role = session.query(Role).filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = create_gravatar_hash(self.email)

    def __repr__(self):
        return "<User %r, %r >" % (self.name, self.id)

    to_dict = mixin_todict    



#class Group(Base):
#    __tablename__ = "groups"
#    pass