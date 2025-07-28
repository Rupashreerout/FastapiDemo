from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from .basic_import import BASE
from sqlalchemy.orm import relationship
from datetime import datetime

class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))  
    gender = Column(String(10)) 
    age = Column(Integer)
    password = Column(String(255))
    role = Column(String(50)) 


    