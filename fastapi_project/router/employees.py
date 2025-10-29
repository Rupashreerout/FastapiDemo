from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from fastapi_project.database import engine
from fastapi_project.models.employee import Employee
from .basic_import import *

Employee.metadata.create_all(bind=engine)
router = APIRouter(prefix="/employees", tags=["Employees"])

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]
    designation: Optional[str]

class EmployeeOut(EmployeeBase):
    id: int
    emp_code: str 
    created_at: datetime

    class Config:
        orm_mode = True


# -------------------- CRUD Routes --------------------


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: db_dependency):
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already exists")

    emp_code = f"EMP-{str(uuid.uuid4())[:8]}"  # e.g., EMP-1a2b3c4d
    new_employee = Employee(emp_code=emp_code, **employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get("/", response_model=List[EmployeeOut])
def get_all_employees(db: db_dependency):
    return db.query(Employee).all()


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: db_dependency):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: db_dependency):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # check email duplication if updating email
    if employee.email and employee.email != db_employee.email:
        existing = db.query(Employee).filter(Employee.email == employee.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: db_dependency):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
