"""
Employee model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    """Employee model representing an employee in the HRMS system."""
    
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship with attendance
    attendance_records = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan"
    )
    
    # Relationship with leaves
    leaves = relationship(
        "Leave",
        foreign_keys="Leave.employee_id",
        back_populates="employee",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', full_name='{self.full_name}')>"
