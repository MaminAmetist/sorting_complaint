from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from database import engine, SessionLocal

Base = declarative_base()

class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    status = Column(String, default='open', insert_default=['open'])
    timestamp = Column(DateTime)
    sentiment = Column(String, default='unknown', insert_default=['positive', 'negative', 'neutral'])
    category = Column(String, default='другое', insert_default=['техническая', 'оплата'])

