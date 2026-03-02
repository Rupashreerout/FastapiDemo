"""
Leave API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app.models.leave import Leave
from app.schemas.leave import (
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse,
    LeaveListResponse,
    LeaveBalanceResponse,
    LeaveStatisticsResponse
)
from app.services.leave_service import LeaveService
from app.core.exceptions import (
    EmployeeNotFoundError,
    ValidationError
)

router = APIRouter()


@router.post(
    "",
    response_model=LeaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Apply for leave",
    description="Create a new leave application"
)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):
    """Apply for leave."""
    try:
        leave_record = LeaveService.create_leave(db, leave)
        # Fetch employee name
        from app.models.employee import Employee
        employee = db.query(Employee).filter(Employee.id == leave_record.employee_id).first()
        leave_dict = {
            **leave_record.__dict__,
            "employee_name": employee.full_name if employee else None
        }
        return LeaveResponse(**leave_dict)
    except (EmployeeNotFoundError, ValidationError) as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating leave: {str(e)}"
        )


@router.get(
    "",
    response_model=LeaveListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all leaves",
    description="Get all leave applications with optional filters"
)
def get_all_leaves(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filter by status: Pending, Approved, Rejected"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date (from)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (to)"),
    db: Session = Depends(get_db)
):
    """Get all leave applications."""
    try:
        # Convert employee_id from string to int if provided and not empty
        employee_id_int = None
        if employee_id and employee_id.strip():
            try:
                employee_id_int = int(employee_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="employee_id must be a valid integer"
                )
        
        # Filter out empty status strings
        status_filter = status if status and status.strip() else None
        
        leaves = LeaveService.get_all_leaves(
            db, skip, limit, status_filter, employee_id_int, start_date, end_date
        )
        
        # Add employee names
        from app.models.employee import Employee
        leave_responses = []
        for leave in leaves:
            employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
            reviewer = None
            if leave.reviewed_by:
                reviewer = db.query(Employee).filter(Employee.id == leave.reviewed_by).first()
            
            leave_dict = {
                **leave.__dict__,
                "employee_name": employee.full_name if employee else None,
                "reviewer_name": reviewer.full_name if reviewer else None
            }
            leave_responses.append(LeaveResponse(**leave_dict))
        
        return LeaveListResponse(count=len(leave_responses), data=leave_responses)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving leaves: {str(e)}"
        )


@router.get(
    "/{leave_id}",
    response_model=LeaveResponse,
    status_code=status.HTTP_200_OK,
    summary="Get leave by ID",
    description="Get a specific leave application by ID"
)
def get_leave_by_id(
    leave_id: int,
    db: Session = Depends(get_db)
):
    """Get leave by ID."""
    try:
        leave = LeaveService.get_leave_by_id(db, leave_id)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Leave with ID {leave_id} not found"
            )
        
        from app.models.employee import Employee
        employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
        reviewer = None
        if leave.reviewed_by:
            reviewer = db.query(Employee).filter(Employee.id == leave.reviewed_by).first()
        
        leave_dict = {
            **leave.__dict__,
            "employee_name": employee.full_name if employee else None,
            "reviewer_name": reviewer.full_name if reviewer else None
        }
        return LeaveResponse(**leave_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving leave: {str(e)}"
        )


@router.put(
    "/{leave_id}/status",
    response_model=LeaveResponse,
    status_code=status.HTTP_200_OK,
    summary="Update leave status",
    description="Approve or reject a leave application"
)
def update_leave_status(
    leave_id: int,
    leave_update: LeaveUpdate,
    db: Session = Depends(get_db)
):
    """Update leave status (Approve/Reject)."""
    try:
        leave = LeaveService.update_leave_status(
            db, leave_id, leave_update.status, leave_update.reviewed_by
        )
        
        from app.models.employee import Employee
        employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
        reviewer = None
        if leave.reviewed_by:
            reviewer = db.query(Employee).filter(Employee.id == leave.reviewed_by).first()
        
        leave_dict = {
            **leave.__dict__,
            "employee_name": employee.full_name if employee else None,
            "reviewer_name": reviewer.full_name if reviewer else None
        }
        return LeaveResponse(**leave_dict)
    except ValidationError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating leave status: {str(e)}"
        )


@router.get(
    "/employee/{employee_id}",
    response_model=LeaveListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee's leaves",
    description="Get all leave applications for a specific employee"
)
def get_employee_leaves(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all leaves for an employee."""
    try:
        leaves = LeaveService.get_all_leaves(db, skip, limit, employee_id=employee_id)
        
        from app.models.employee import Employee
        leave_responses = []
        for leave in leaves:
            employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
            reviewer = None
            if leave.reviewed_by:
                reviewer = db.query(Employee).filter(Employee.id == leave.reviewed_by).first()
            
            leave_dict = {
                **leave.__dict__,
                "employee_name": employee.full_name if employee else None,
                "reviewer_name": reviewer.full_name if reviewer else None
            }
            leave_responses.append(LeaveResponse(**leave_dict))
        
        return LeaveListResponse(count=len(leave_responses), data=leave_responses)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving employee leaves: {str(e)}"
        )


@router.get(
    "/employee/{employee_id}/balance",
    response_model=LeaveBalanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee leave balance",
    description="Get leave balance for a specific employee"
)
def get_employee_leave_balance(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get leave balance for an employee."""
    try:
        balance = LeaveService.get_employee_leave_balance(db, employee_id)
        return LeaveBalanceResponse(**balance)
    except EmployeeNotFoundError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving leave balance: {str(e)}"
        )


@router.get(
    "/statistics",
    response_model=LeaveStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get leave statistics",
    description="Get overall leave statistics"
)
def get_leave_statistics(
    db: Session = Depends(get_db)
):
    """Get leave statistics."""
    try:
        stats = LeaveService.get_leave_statistics(db)
        return LeaveStatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving leave statistics: {str(e)}"
        )
