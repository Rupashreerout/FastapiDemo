from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi_project.models.customer import Customer

from typing import Optional
from datetime import datetime
from pydantic import BaseModel,EmailStr
from fastapi_project.database import SessionLocal,engine
from .basic_import import *
Customer.metadata.create_all(bind=engine)
router=APIRouter()

class CustomerBase(BaseModel):
    name:str
    email:EmailStr
    age:int
    phone:str
class CustomerCreate(CustomerBase):
    pass 
class CustomerUpdate(BaseModel):
    name:Optional[str]
    age:Optional[int]
    phone:Optional[str]

class CustomerOut(CustomerBase):
    id:int
    created_at: datetime 

    class Config:
        orm_mode=True


@router.post("/",response_model=CustomerOut)
def create_customer(customer:CustomerCreate,db:db_dependency):
    db_customer=db.query(Customer).filter(Customer.email==customer.email).first()
    if db_customer:raise HTTPException(status_code=400,detail="Email already exist")
    new_customer=Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/",response_model=list[CustomerOut])
def get_customer(db:db_dependency):
    return db.query(Customer).all()

@router.get("/{customer_id}",response_model=CustomerOut)
def get_customer(customer_id:int,db:db_dependency):
    customer=db.query(Customer).filter(Customer.id==customer_id).first()
    if not customer:raise HTTPException(status_code=404,detail="Customer not found")
    return customer

@router.put("/{customer_id}",response_model=CustomerOut)
def update_customer(customer_id:int,customer:CustomerUpdate,db:db_dependency):
    db_customer=db.query(Customer).filter(Customer.id == customer_id ).first()
    if not db_customer:raise HTTPException(status_code=404,detail="Customer not found")
    for key,value in customer.dict(exclude_unset=True).items():
        setattr(db_customer,key,value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
@router.delete("/{customer_id}")
def delete_customer(customer_id:int,db:db_dependency):
    db_customer=db.query(Customer).filter(Customer.id==customer_id).first()
    if not db_customer:raise HTTPException(status_code=404,detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return{"massage":"Customer Deleted Successfully"}    
    