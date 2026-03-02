"""
Custom exception classes for the application.
"""
from fastapi import HTTPException, status


class EmployeeNotFoundError(HTTPException):
    """Raised when an employee is not found."""
    
    def __init__(self, employee_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )


class EmployeeAlreadyExistsError(HTTPException):
    """Raised when trying to create an employee that already exists."""
    
    def __init__(self, message: str = "Employee already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class AttendanceNotFoundError(HTTPException):
    """Raised when an attendance record is not found."""
    
    def __init__(self, message: str = "Attendance record not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class AttendanceAlreadyExistsError(HTTPException):
    """Raised when trying to create a duplicate attendance record."""
    
    def __init__(self, message: str = "Attendance record already exists for this employee and date"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class ValidationError(HTTPException):
    """Raised when validation fails."""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
