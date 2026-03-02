"""
Leave model definition.
"""
from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Leave(Base):
    """Leave model representing leave applications for employees."""
    
    __tablename__ = "leaves"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    leave_type = Column(String(50), nullable=False)  # Annual, Sick, Casual, Emergency
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Numeric(5, 2), nullable=False)
    status = Column(String(20), nullable=False, default="Pending")  # Pending, Approved, Rejected
    reason = Column(String(500), nullable=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="leaves")
    reviewer = relationship("Employee", foreign_keys=[reviewed_by])
    
    def __repr__(self):
        return f"<Leave(id={self.id}, employee_id={self.employee_id}, leave_type='{self.leave_type}', status='{self.status}')>"
