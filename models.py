from sqlalchemy import Column,String,Integer,Text,DateTime,Boolean,ForeignKey
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    password = Column(String)
    email = Column(String,unique=True)
    is_active = Column(Boolean,default=True)
    is_superuser = Column(Boolean,default=False)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("User",back_populates="posts")
