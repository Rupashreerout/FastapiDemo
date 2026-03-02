"""
Attendance service layer for business logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional
from datetime import date

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate
from app.core.exceptions import (
    AttendanceNotFoundError,
    AttendanceAlreadyExistsError,
    EmployeeNotFoundError,
    ValidationError
)


class AttendanceService:
    """Service class for attendance-related operations."""
    
    @staticmethod
    def create_attendance(db: Session, attendance_data: AttendanceCreate) -> Attendance:
        """
        Create a new attendance record.
        
        Args:
            db: Database session
            attendance_data: Attendance creation data
            
        Returns:
            Created attendance object
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
            AttendanceAlreadyExistsError: If attendance already exists for this date
        """
        # Check if employee exists
        employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
        
        if not employee:
            raise EmployeeNotFoundError(attendance_data.employee_id)
        
        # Check if attendance already exists for this employee and date
        existing_attendance = db.query(Attendance).filter(
            Attendance.employee_id == attendance_data.employee_id,
            Attendance.date == attendance_data.date
        ).first()
        
        if existing_attendance:
            raise AttendanceAlreadyExistsError()
        
        # Validate status
        if attendance_data.status not in ["Present", "Absent"]:
            raise ValidationError("Status must be either 'Present' or 'Absent'")
        
        # Create new attendance record
        db_attendance = Attendance(
            employee_id=attendance_data.employee_id,
            date=attendance_data.date,
            status=attendance_data.status
        )
        
        try:
            db.add(db_attendance)
            db.commit()
            db.refresh(db_attendance)
            return db_attendance
        except IntegrityError as e:
            db.rollback()
            raise AttendanceAlreadyExistsError()
    
    @staticmethod
    def get_all_attendance(db: Session, skip: int = 0, limit: int = 100) -> List[Attendance]:
        """
        Get all attendance records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance objects
        """
        return db.query(Attendance).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_attendance_by_employee_id(
        db: Session,
        employee_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance objects
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
        """
        # Check if employee exists
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        
        return db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_attendance_summary(db: Session, employee_id: int) -> dict:
        """
        Get attendance summary for an employee (total present days).
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            Dictionary with employee_id and total_present_days
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
        """
        # Check if employee exists
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        
        # Count present days
        total_present = db.query(func.count(Attendance.id)).filter(
            Attendance.employee_id == employee_id,
            Attendance.status == "Present"
        ).scalar() or 0
        
        return {
            "employee_id": employee_id,
            "total_present_days": total_present
        }
    
    @staticmethod
    def get_attendance_by_date_range(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records filtered by date range.
        
        Args:
            db: Database session
            start_date: Start date (optional)
            end_date: End date (optional)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance objects
        """
        query = db.query(Attendance)
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        return query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_attendance_by_date(
        db: Session,
        attendance_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records for a specific date.
        
        Args:
            db: Database session
            attendance_date: Date to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance objects
        """
        return db.query(Attendance).filter(
            Attendance.date == attendance_date
        ).order_by(Attendance.employee_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_employees_summary(db: Session) -> List[dict]:
        """
        Get attendance summary for all employees (total present days).
        
        Args:
            db: Database session
            
        Returns:
            List of dictionaries with employee_id and total_present_days
        """
        # Get all employees
        employees = db.query(Employee).all()
        
        summaries = []
        for employee in employees:
            total_present = db.query(func.count(Attendance.id)).filter(
                Attendance.employee_id == employee.id,
                Attendance.status == "Present"
            ).scalar() or 0
            
            total_absent = db.query(func.count(Attendance.id)).filter(
                Attendance.employee_id == employee.id,
                Attendance.status == "Absent"
            ).scalar() or 0
            
            summaries.append({
                "employee_id": employee.id,
                "employee_name": employee.full_name,
                "employee_code": employee.employee_id,
                "department": employee.department,
                "total_present_days": total_present,
                "total_absent_days": total_absent,
                "total_days": total_present + total_absent
            })
        
        return summaries
