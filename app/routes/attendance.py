"""
Attendance API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceListResponse,
    AttendanceDetailResponse,
    AttendanceSummaryResponse
)
from app.services.attendance_service import AttendanceService
from app.core.exceptions import (
    AttendanceNotFoundError,
    AttendanceAlreadyExistsError,
    EmployeeNotFoundError
)

router = APIRouter()


@router.post(
    "/",
    response_model=AttendanceDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance",
    description="Create a new attendance record for an employee"
)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    """
    Mark attendance for an employee.
    
    - **employee_id**: ID of the employee
    - **date**: Date of attendance (YYYY-MM-DD)
    - **status**: Attendance status ("Present" or "Absent")
    """
    try:
        db_attendance = AttendanceService.create_attendance(db, attendance)
        return AttendanceDetailResponse(data=db_attendance)
    except (EmployeeNotFoundError, AttendanceAlreadyExistsError) as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while marking attendance: {str(e)}"
        )


@router.get(
    "/",
    response_model=AttendanceListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all attendance records",
    description="Retrieve a list of all attendance records with pagination and optional date filtering"
)
def get_all_attendance(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="Filter records from this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter records until this date (YYYY-MM-DD)"),
    attendance_date: Optional[date] = Query(None, description="Filter records for a specific date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get all attendance records with optional date filtering.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    - **start_date**: Filter from this date (optional)
    - **end_date**: Filter until this date (optional)
    - **attendance_date**: Filter for a specific date (optional, takes precedence over date range)
    """
    if attendance_date:
        attendance_records = AttendanceService.get_attendance_by_date(
            db, attendance_date, skip=skip, limit=limit
        )
    elif start_date or end_date:
        attendance_records = AttendanceService.get_attendance_by_date_range(
            db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
        )
    else:
        attendance_records = AttendanceService.get_all_attendance(db, skip=skip, limit=limit)
    
    return AttendanceListResponse(count=len(attendance_records), data=attendance_records)


@router.get(
    "/employee/{employee_id}",
    response_model=AttendanceListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get attendance by employee",
    description="Retrieve all attendance records for a specific employee"
)
def get_attendance_by_employee(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get attendance records for a specific employee.
    
    - **employee_id**: The ID of the employee
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        attendance_records = AttendanceService.get_attendance_by_employee_id(
            db, employee_id, skip=skip, limit=limit
        )
        return AttendanceListResponse(count=len(attendance_records), data=attendance_records)
    except EmployeeNotFoundError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving attendance: {str(e)}"
        )


@router.get(
    "/employee/{employee_id}/summary",
    response_model=AttendanceSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get attendance summary",
    description="Get attendance summary (total present days) for an employee"
)
def get_attendance_summary(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Get attendance summary for an employee.
    
    - **employee_id**: The ID of the employee
    
    Returns the total number of present days for the employee.
    """
    try:
        summary = AttendanceService.get_attendance_summary(db, employee_id)
        return AttendanceSummaryResponse(**summary)
    except EmployeeNotFoundError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving attendance summary: {str(e)}"
        )


@router.get(
    "/employees/summary",
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    summary="Get attendance summary for all employees",
    description="Get total present days for all employees"
)
def get_all_employees_summary(
    db: Session = Depends(get_db)
):
    """
    Get attendance summary for all employees.
    
    Returns a list with total present days, absent days, and total days for each employee.
    """
    try:
        summaries = AttendanceService.get_all_employees_summary(db)
        return summaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving employee summaries: {str(e)}"
        )
