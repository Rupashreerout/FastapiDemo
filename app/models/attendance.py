"""
Attendance model definition.
"""
from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Attendance(Base):
    """Attendance model representing attendance records for employees."""
    
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # "Present" or "Absent"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship with employee
    employee = relationship("Employee", back_populates="attendance_records")
    
    # Unique constraint: one attendance record per employee per date
    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
    )
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date='{self.date}', status='{self.status}')>"
