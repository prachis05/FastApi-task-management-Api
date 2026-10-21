from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__="tasks"
    id  = Column(Integer,primary_key=True,index=True)
    title=Column(String, nullable=False)
    description=Column(String, nullable=False)
    status = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

