"""
Employee API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    EmployeeDetailResponse
)
from app.services.employee_service import EmployeeService
from app.core.exceptions import (
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError
)

router = APIRouter()


@router.post(
    "/",
    response_model=EmployeeDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Create a new employee with employee_id, full_name, email, and department"
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new employee.
    
    - **employee_id**: Unique identifier for the employee (required, unique)
    - **full_name**: Full name of the employee (required)
    - **email**: Email address (required, unique, valid format)
    - **department**: Department name (required)
    """
    try:
        db_employee = EmployeeService.create_employee(db, employee)
        return EmployeeDetailResponse(data=db_employee)
    except EmployeeAlreadyExistsError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating employee: {str(e)}"
        )


@router.get(
    "/",
    response_model=EmployeeListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all employees",
    description="Retrieve a list of all employees with pagination"
)
def get_all_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all employees.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    employees = EmployeeService.get_all_employees(db, skip=skip, limit=limit)
    return EmployeeListResponse(count=len(employees), data=employees)


@router.get(
    "/{employee_id}",
    response_model=EmployeeDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID",
    description="Retrieve a specific employee by their ID"
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Get employee by ID.
    
    - **employee_id**: The ID of the employee to retrieve
    """
    db_employee = EmployeeService.get_employee_by_id(db, employee_id)
    
    if not db_employee:
        raise EmployeeNotFoundError(employee_id)
    
    return EmployeeDetailResponse(data=db_employee)


@router.put(
    "/{employee_id}",
    response_model=EmployeeDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an employee",
    description="Update an employee by their ID"
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an employee by ID.
    
    - **employee_id**: The ID of the employee to update
    - All fields in the request body are optional
    """
    try:
        db_employee = EmployeeService.update_employee(db, employee_id, employee)
        return EmployeeDetailResponse(data=db_employee)
    except EmployeeNotFoundError as e:
        raise e
    except EmployeeAlreadyExistsError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating employee: {str(e)}"
        )


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an employee",
    description="Delete an employee by their ID"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an employee by ID.
    
    - **employee_id**: The ID of the employee to delete
    
    Returns a success message if deletion is successful.
    """
    try:
        EmployeeService.delete_employee(db, employee_id)
        return {
            "success": True,
            "message": f"Employee with ID {employee_id} deleted successfully"
        }
    except EmployeeNotFoundError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting employee: {str(e)}"
        )
