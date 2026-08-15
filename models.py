from sqlalchemy import Column , Integer , String , Boolean , ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base




class User(Base):
    __tablename__= "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,nullable=False,index=True)
    username =Column(String,unique=True,nullable=False,index=True)
    hashed_password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=True) # can have without description
    completed = Column(Boolean,default=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
