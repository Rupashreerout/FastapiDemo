from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from.basic_import import BASE
import enum


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"


class Employee(BASE):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String(20), unique=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    department = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 
    # Relationship with Attendance
    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")


class Attendance(BASE):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 
    # Relationship with Employee
    employee = relationship("Employee", back_populates="attendance_records")
