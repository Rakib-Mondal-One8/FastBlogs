from database import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)
    role = Column(String)


class Blogs(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)
    author = Column(String)
    category = Column(String)
    image_url = Column(String,nullable=True)
    user_id = Column(Integer,ForeignKey("users.id"))


class Readers(Base):
    __tablename__ = 'readers'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    