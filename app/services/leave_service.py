"""
Leave service layer for business logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.models.leave import Leave
from app.models.employee import Employee
from app.schemas.leave import LeaveCreate, LeaveUpdate
from app.core.exceptions import (
    EmployeeNotFoundError,
    ValidationError
)


class LeaveService:
    """Service class for leave-related operations."""
    
    # Default leave balances per year
    DEFAULT_LEAVE_BALANCES = {
        "Annual": 12,
        "Sick": 10,
        "Casual": 5,
        "Emergency": 3
    }
    
    @staticmethod
    def create_leave(db: Session, leave_data: LeaveCreate) -> Leave:
        """
        Create a new leave application.
        
        Args:
            db: Database session
            leave_data: Leave creation data
            
        Returns:
            Created leave object
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
            ValidationError: If validation fails
        """
        # Check if employee exists
        employee = db.query(Employee).filter(Employee.id == leave_data.employee_id).first()
        if not employee:
            raise EmployeeNotFoundError(leave_data.employee_id)
        
        # Validate dates
        if leave_data.start_date > leave_data.end_date:
            raise ValidationError("Start date must be before or equal to end date")
        
        if leave_data.start_date < date.today():
            raise ValidationError("Cannot apply for leave in the past")
        
        # Calculate days (excluding weekends)
        days = LeaveService._calculate_working_days(leave_data.start_date, leave_data.end_date)
        
        if days <= 0:
            raise ValidationError("Invalid date range")
        
        # Check leave balance
        balance = LeaveService.get_employee_leave_balance(db, leave_data.employee_id)
        leave_type_key = leave_data.leave_type.lower().replace(" ", "_")
        
        # balance is a dictionary, access it with bracket notation
        if leave_type_key == "annual" and balance["annual_leave_remaining"] < days:
            raise ValidationError(f"Insufficient annual leave balance. Available: {balance['annual_leave_remaining']}")
        elif leave_type_key == "sick" and balance["sick_leave_remaining"] < days:
            raise ValidationError(f"Insufficient sick leave balance. Available: {balance['sick_leave_remaining']}")
        elif leave_type_key == "casual" and balance["casual_leave_remaining"] < days:
            raise ValidationError(f"Insufficient casual leave balance. Available: {balance['casual_leave_remaining']}")
        elif leave_type_key == "emergency" and balance["emergency_leave_remaining"] < days:
            raise ValidationError(f"Insufficient emergency leave balance. Available: {balance['emergency_leave_remaining']}")
        
        # Create leave record
        db_leave = Leave(
            employee_id=leave_data.employee_id,
            leave_type=leave_data.leave_type,
            start_date=leave_data.start_date,
            end_date=leave_data.end_date,
            days=Decimal(str(days)),
            reason=leave_data.reason,
            status="Pending"
        )
        
        db.add(db_leave)
        db.commit()
        db.refresh(db_leave)
        return db_leave
    
    @staticmethod
    def _calculate_working_days(start_date: date, end_date: date) -> Decimal:
        """Calculate working days excluding weekends."""
        days = Decimal('0')
        current = start_date
        while current <= end_date:
            # Monday = 0, Sunday = 6
            if current.weekday() < 5:  # Monday to Friday
                days += Decimal('1')
            current += timedelta(days=1)
        return days
    
    @staticmethod
    def get_all_leaves(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        employee_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Leave]:
        """
        Get all leave records with filters.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            employee_id: Filter by employee ID
            start_date: Filter by start date (from)
            end_date: Filter by end date (to)
            
        Returns:
            List of leave objects
        """
        query = db.query(Leave)
        
        if status:
            query = query.filter(Leave.status == status)
        if employee_id:
            query = query.filter(Leave.employee_id == employee_id)
        if start_date:
            query = query.filter(Leave.start_date >= start_date)
        if end_date:
            query = query.filter(Leave.end_date <= end_date)
        
        return query.order_by(Leave.applied_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_leave_by_id(db: Session, leave_id: int) -> Optional[Leave]:
        """Get leave by ID."""
        return db.query(Leave).filter(Leave.id == leave_id).first()
    
    @staticmethod
    def update_leave_status(
        db: Session,
        leave_id: int,
        status: str,
        reviewed_by: Optional[int] = None
    ) -> Leave:
        """
        Update leave status (Approve/Reject).
        
        Args:
            db: Database session
            leave_id: Leave ID
            status: New status (Approved/Rejected)
            reviewed_by: ID of reviewer
            
        Returns:
            Updated leave object
            
        Raises:
            ValidationError: If status is invalid
        """
        leave = db.query(Leave).filter(Leave.id == leave_id).first()
        if not leave:
            raise ValidationError(f"Leave with ID {leave_id} not found")
        
        if status not in ["Approved", "Rejected"]:
            raise ValidationError("Status must be either 'Approved' or 'Rejected'")
        
        leave.status = status
        leave.reviewed_by = reviewed_by
        leave.reviewed_at = datetime.now()
        
        db.commit()
        db.refresh(leave)
        return leave
    
    @staticmethod
    def get_employee_leave_balance(db: Session, employee_id: int) -> dict:
        """
        Get leave balance for an employee.
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            Dictionary with leave balances
        """
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        
        # Get current year
        current_year = date.today().year
        
        # Get approved leaves for current year
        approved_leaves = db.query(Leave).filter(
            and_(
                Leave.employee_id == employee_id,
                Leave.status == "Approved",
                func.extract('year', Leave.start_date) == current_year
            )
        ).all()
        
        # Calculate used leaves by type
        annual_used = sum([float(leave.days) for leave in approved_leaves if leave.leave_type == "Annual"])
        sick_used = sum([float(leave.days) for leave in approved_leaves if leave.leave_type == "Sick"])
        casual_used = sum([float(leave.days) for leave in approved_leaves if leave.leave_type == "Casual"])
        emergency_used = sum([float(leave.days) for leave in approved_leaves if leave.leave_type == "Emergency"])
        
        return {
            "employee_id": employee_id,
            "employee_name": employee.full_name,
            "annual_leave_total": LeaveService.DEFAULT_LEAVE_BALANCES["Annual"],
            "annual_leave_used": Decimal(str(annual_used)),
            "annual_leave_remaining": Decimal(str(LeaveService.DEFAULT_LEAVE_BALANCES["Annual"] - annual_used)),
            "sick_leave_total": LeaveService.DEFAULT_LEAVE_BALANCES["Sick"],
            "sick_leave_used": Decimal(str(sick_used)),
            "sick_leave_remaining": Decimal(str(LeaveService.DEFAULT_LEAVE_BALANCES["Sick"] - sick_used)),
            "casual_leave_total": LeaveService.DEFAULT_LEAVE_BALANCES["Casual"],
            "casual_leave_used": Decimal(str(casual_used)),
            "casual_leave_remaining": Decimal(str(LeaveService.DEFAULT_LEAVE_BALANCES["Casual"] - casual_used)),
            "emergency_leave_total": LeaveService.DEFAULT_LEAVE_BALANCES["Emergency"],
            "emergency_leave_used": Decimal(str(emergency_used)),
            "emergency_leave_remaining": Decimal(str(LeaveService.DEFAULT_LEAVE_BALANCES["Emergency"] - emergency_used)),
        }
    
    @staticmethod
    def get_leave_statistics(db: Session) -> dict:
        """
        Get leave statistics.
        
        Returns:
            Dictionary with leave statistics
        """
        total_leaves = db.query(func.count(Leave.id)).scalar() or 0
        pending_leaves = db.query(func.count(Leave.id)).filter(Leave.status == "Pending").scalar() or 0
        approved_leaves = db.query(func.count(Leave.id)).filter(Leave.status == "Approved").scalar() or 0
        rejected_leaves = db.query(func.count(Leave.id)).filter(Leave.status == "Rejected").scalar() or 0
        
        # Leaves by type
        leaves_by_type = {}
        for leave_type in ["Annual", "Sick", "Casual", "Emergency"]:
            count = db.query(func.count(Leave.id)).filter(Leave.leave_type == leave_type).scalar() or 0
            leaves_by_type[leave_type] = count
        
        # Pending leaves by employee
        pending_query = db.query(
            Leave.employee_id,
            Employee.full_name,
            func.count(Leave.id).label('count')
        ).join(Employee).filter(
            Leave.status == "Pending"
        ).group_by(Leave.employee_id, Employee.full_name).all()
        
        pending_by_employee = [
            {"employee_id": emp_id, "employee_name": name, "count": count}
            for emp_id, name, count in pending_query
        ]
        
        return {
            "total_leaves": total_leaves,
            "pending_leaves": pending_leaves,
            "approved_leaves": approved_leaves,
            "rejected_leaves": rejected_leaves,
            "leaves_by_type": leaves_by_type,
            "pending_by_employee": pending_by_employee
        }
