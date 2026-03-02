"""
Employee service layer for business logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.exceptions import (
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError,
    ValidationError
)


class EmployeeService:
    """Service class for employee-related operations."""
    
    @staticmethod
    def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
        """
        Create a new employee.
        
        Args:
            db: Database session
            employee_data: Employee creation data
            
        Returns:
            Created employee object
            
        Raises:
            EmployeeAlreadyExistsError: If employee_id or email already exists
            ValidationError: If validation fails
        """
        # Check if employee_id already exists
        existing_employee = db.query(Employee).filter(
            Employee.employee_id == employee_data.employee_id
        ).first()
        
        if existing_employee:
            raise EmployeeAlreadyExistsError(
                f"Employee with employee_id '{employee_data.employee_id}' already exists"
            )
        
        # Check if email already exists
        existing_email = db.query(Employee).filter(
            Employee.email == employee_data.email
        ).first()
        
        if existing_email:
            raise EmployeeAlreadyExistsError(
                f"Employee with email '{employee_data.email}' already exists"
            )
        
        # Create new employee
        db_employee = Employee(
            employee_id=employee_data.employee_id,
            full_name=employee_data.full_name,
            email=employee_data.email,
            department=employee_data.department
        )
        
        try:
            db.add(db_employee)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except IntegrityError as e:
            db.rollback()
            raise EmployeeAlreadyExistsError(
                "Employee with this employee_id or email already exists"
            )
    
    @staticmethod
    def get_employee_by_id(db: Session, employee_id: int) -> Optional[Employee]:
        """
        Get employee by ID.
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            Employee object or None if not found
        """
        return db.query(Employee).filter(Employee.id == employee_id).first()
    
    @staticmethod
    def get_all_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Get all employees with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of employee objects
        """
        return db.query(Employee).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        """
        Delete an employee by ID.
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            EmployeeNotFoundError: If employee not found
        """
        db_employee = EmployeeService.get_employee_by_id(db, employee_id)
        
        if not db_employee:
            raise EmployeeNotFoundError(employee_id)
        
        db.delete(db_employee)
        db.commit()
        return True
    
    @staticmethod
    def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate) -> Employee:
        """
        Update an employee by ID.
        
        Args:
            db: Database session
            employee_id: Employee ID
            employee_data: Employee update data (all fields optional)
            
        Returns:
            Updated employee object
            
        Raises:
            EmployeeNotFoundError: If employee not found
            EmployeeAlreadyExistsError: If employee_id or email already exists
        """
        db_employee = EmployeeService.get_employee_by_id(db, employee_id)
        
        if not db_employee:
            raise EmployeeNotFoundError(employee_id)
        
        # Update fields if provided
        update_data = employee_data.model_dump(exclude_unset=True)
        
        # Check for duplicate employee_id if being updated
        if 'employee_id' in update_data and update_data['employee_id'] != db_employee.employee_id:
            existing = db.query(Employee).filter(
                Employee.employee_id == update_data['employee_id']
            ).first()
            if existing:
                raise EmployeeAlreadyExistsError(
                    f"Employee with employee_id '{update_data['employee_id']}' already exists"
                )
        
        # Check for duplicate email if being updated
        if 'email' in update_data and update_data['email'] != db_employee.email:
            existing = db.query(Employee).filter(
                Employee.email == update_data['email']
            ).first()
            if existing:
                raise EmployeeAlreadyExistsError(
                    f"Employee with email '{update_data['email']}' already exists"
                )
        
        # Update the employee
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        
        try:
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except IntegrityError as e:
            db.rollback()
            raise EmployeeAlreadyExistsError(
                "Employee with this employee_id or email already exists"
            )
    
    @staticmethod
    def get_employee_by_employee_id(db: Session, employee_id: str) -> Optional[Employee]:
        """
        Get employee by employee_id (string identifier).
        
        Args:
            db: Database session
            employee_id: Employee identifier string
            
        Returns:
            Employee object or None if not found
        """
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()
