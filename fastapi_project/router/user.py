from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_project.models.user import User
from passlib.hash import bcrypt
from jose import jwt
from typing import List, Optional
from pydantic import BaseModel
from fastapi_project.database import SessionLocal, engine
from .basic_import import *

User.metadata.create_all(bind=engine)
router = APIRouter()




class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    gender: str
    age: int
    password: str
    role: str

class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    password: Optional[str]
    role: Optional[str]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True



@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: db_dependency):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        gender=user.gender,
        age=user.age,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserResponse])
def get_users(db: db_dependency):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user_update).items():
        if value is not None:
            if var == "password":
                setattr(user, var, bcrypt.hash(value))
            else:
                setattr(user, var, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id:int,db:db_dependency):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:raise HTTPException(status_code=404,detail="User not found")
    db.delete(db_user)
    db.commit()
    return{"massage":"User Deleted Successfully"}    