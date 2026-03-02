"""
Pydantic schemas for Dashboard.
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime


class DashboardStatsResponse(BaseModel):
    """Schema for dashboard statistics response."""
    success: bool = True
    total_employees: int
    total_attendance_records: int
    total_present_today: int
    total_absent_today: int
    average_attendance_rate: float
    employees_by_department: Dict[str, int]
    this_week_summary: Dict[str, int]
    recent_employees: List[Dict]
    recent_attendance: List[Dict]
    pending_leaves: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeSummaryResponse(BaseModel):
    """Schema for employee attendance summary."""
    employee_id: int
    employee_name: str
    employee_code: str
    department: str
    total_present_days: int
    total_absent_days: int
    total_days: int
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeSummaryListResponse(BaseModel):
    """Schema for list of employee summaries."""
    success: bool = True
    count: int
    data: List["EmployeeSummaryResponse"]
    
    model_config = ConfigDict(from_attributes=True)
