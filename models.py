from sqlalchemy import Column,String,Integer,Text,DateTime
from database import Base
from sqlalchemy.sql import func



class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)




