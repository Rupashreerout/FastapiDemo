"""
Pydantic schemas for Leave model.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class LeaveBase(BaseModel):
    """Base schema for Leave with common fields."""
    employee_id: int
    leave_type: str = Field(..., description="Type of leave: Annual, Sick, Casual, Emergency")
    start_date: date
    end_date: date
    reason: Optional[str] = Field(None, max_length=500)


class LeaveCreate(LeaveBase):
    """Schema for creating a new leave application."""
    pass


class LeaveUpdate(BaseModel):
    """Schema for updating leave status."""
    status: str = Field(..., description="Status: Pending, Approved, Rejected")
    reviewed_by: Optional[int] = None


class LeaveResponse(LeaveBase):
    """Schema for leave response."""
    id: int
    days: Decimal
    status: str
    applied_at: datetime
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    employee_name: Optional[str] = None
    reviewer_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class LeaveListResponse(BaseModel):
    """Schema for list of leaves response."""
    success: bool = True
    count: int
    data: list[LeaveResponse]
    
    model_config = ConfigDict(from_attributes=True)


class LeaveBalanceResponse(BaseModel):
    """Schema for leave balance response."""
    employee_id: int
    employee_name: str
    annual_leave_total: int = 12
    annual_leave_used: Decimal = Decimal('0')
    annual_leave_remaining: Decimal
    sick_leave_total: int = 10
    sick_leave_used: Decimal = Decimal('0')
    sick_leave_remaining: Decimal
    casual_leave_total: int = 5
    casual_leave_used: Decimal = Decimal('0')
    casual_leave_remaining: Decimal
    emergency_leave_total: int = 3
    emergency_leave_used: Decimal = Decimal('0')
    emergency_leave_remaining: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class LeaveStatisticsResponse(BaseModel):
    """Schema for leave statistics response."""
    total_leaves: int
    pending_leaves: int
    approved_leaves: int
    rejected_leaves: int
    leaves_by_type: dict
    pending_by_employee: list[dict]
    
    model_config = ConfigDict(from_attributes=True)
