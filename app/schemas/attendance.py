"""
Pydantic schemas for Attendance model.
"""
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class AttendanceBase(BaseModel):
    """Base schema for Attendance with common fields."""
    employee_id: int
    date: date
    status: str


class AttendanceCreate(AttendanceBase):
    """Schema for creating a new attendance record."""
    pass


class AttendanceResponse(AttendanceBase):
    """Schema for attendance response."""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceListResponse(BaseModel):
    """Schema for list of attendance records response."""
    success: bool = True
    count: int
    data: list["AttendanceResponse"]
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceDetailResponse(BaseModel):
    """Schema for single attendance detail response."""
    success: bool = True
    data: "AttendanceResponse"
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceSummaryResponse(BaseModel):
    """Schema for attendance summary response."""
    success: bool = True
    employee_id: int
    total_present_days: int
    
    model_config = ConfigDict(from_attributes=True)
