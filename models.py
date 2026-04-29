from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class Machines(Base):
    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    machine_data = Column(Text)