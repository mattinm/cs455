from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'user'
    
class Patient(Base):
    