from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from pydantic import BaseModel
from enum import Enum
from fastapi_project.database import engine
from fastapi_project.models.employee import Attendance
from fastapi_project.models.employee import Employee
from .basic_import import *

Attendance.metadata.create_all(bind=engine)
router = APIRouter(prefix="/attendance", tags=["Attendance"])

# -------------------- Schemas --------------------
class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# -------------------- CRUD Routes --------------------
@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def mark_attendance(attendance: AttendanceCreate, db: db_dependency):
    employee = db.query(Employee).filter(Employee.id == attendance.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(Attendance).filter(
        Attendance.employee_id == attendance.employee_id,
        Attendance.date == attendance.date
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    new_attendance = Attendance(**attendance.dict())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


@router.get("/", response_model=List[AttendanceOut])
def get_all_attendance(db: db_dependency):
    return db.query(Attendance).order_by(Attendance.date.desc()).all()


@router.get("/{employee_id}", response_model=List[AttendanceOut])
def get_employee_attendance(employee_id: int, db: db_dependency):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).order_by(Attendance.date.desc()).all()
    return records


@router.get("/date/{date}", response_model=List[AttendanceOut])
def get_attendance_by_date(date: date, db: db_dependency):
    records = db.query(Attendance).filter(Attendance.date == date).all()
    return records


@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: db_dependency):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(db_attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}
