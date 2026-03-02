"""
Pydantic schemas for Employee model.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class EmployeeBase(BaseModel):
    """Base schema for Employee with common fields."""
    employee_id: str = Field(..., min_length=1, max_length=50, description="Unique employee identifier")
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name of the employee")
    email: EmailStr = Field(..., description="Email address of the employee")
    department: str = Field(..., min_length=1, max_length=100, description="Department name")


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee."""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee (all fields optional)."""
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)


class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeListResponse(BaseModel):
    """Schema for list of employees response."""
    success: bool = True
    count: int
    data: list["EmployeeResponse"]
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeDetailResponse(BaseModel):
    """Schema for single employee detail response."""
    success: bool = True
    data: "EmployeeResponse"
    
    model_config = ConfigDict(from_attributes=True)
