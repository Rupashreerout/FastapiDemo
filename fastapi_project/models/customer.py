from sqlalchemy import Column,Integer,String,DateTime,func
from.basic_import import BASE

class Customer(BASE):
    __tablename__="customers"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    email=Column(String(100),unique=True,index=True)
    age=Column(Integer)
    phone=Column(String(15))
    created_at = Column(DateTime(timezone=True), server_default=func.now())