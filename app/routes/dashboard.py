"""
Dashboard API routes.
"""
from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.leave import Leave
from app.schemas.dashboard import DashboardStatsResponse, EmployeeSummaryResponse
from app.services.attendance_service import AttendanceService

router = APIRouter()


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get dashboard statistics",
    description="Get overall statistics for the dashboard"
)
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics.
    
    Returns:
    - Total employees
    - Total attendance records
    - Total present today
    - Total absent today
    - Average attendance rate
    - Employees by department
    - This week summary
    - Recent employees (last 5)
    - Recent attendance (last 5)
    """
    try:
        # Get total employees
        total_employees = db.query(func.count(Employee.id)).scalar() or 0
        
        # Get total attendance records
        total_attendance_records = db.query(func.count(Attendance.id)).scalar() or 0
        
        # Get today's date
        today = date.today()
        
        # Get today's present count
        total_present_today = db.query(func.count(Attendance.id)).filter(
            Attendance.date == today,
            Attendance.status == "Present"
        ).scalar() or 0
        
        # Get today's absent count
        total_absent_today = db.query(func.count(Attendance.id)).filter(
            Attendance.date == today,
            Attendance.status == "Absent"
        ).scalar() or 0
        
        # Calculate average attendance rate
        total_present_all = db.query(func.count(Attendance.id)).filter(
            Attendance.status == "Present"
        ).scalar() or 0
        
        total_attendance_all = db.query(func.count(Attendance.id)).scalar() or 0
        
        average_attendance_rate = 0.0
        if total_attendance_all > 0:
            average_attendance_rate = round((total_present_all / total_attendance_all) * 100, 2)
        
        # Get employees by department
        dept_counts = db.query(
            Employee.department,
            func.count(Employee.id).label('count')
        ).group_by(Employee.department).all()
        
        employees_by_department = {dept: count for dept, count in dept_counts}
        
        # Get this week summary (last 7 days)
        week_start = today - timedelta(days=6)
        this_week_present = db.query(func.count(Attendance.id)).filter(
            Attendance.date >= week_start,
            Attendance.date <= today,
            Attendance.status == "Present"
        ).scalar() or 0
        
        this_week_absent = db.query(func.count(Attendance.id)).filter(
            Attendance.date >= week_start,
            Attendance.date <= today,
            Attendance.status == "Absent"
        ).scalar() or 0
        
        this_week_summary = {
            "present": this_week_present,
            "absent": this_week_absent
        }
        
        # Get recent employees (last 5)
        recent_employees_query = db.query(Employee).order_by(
            Employee.created_at.desc()
        ).limit(5).all()
        
        recent_employees = [
            {
                "id": emp.id,
                "employee_id": emp.employee_id,
                "full_name": emp.full_name,
                "department": emp.department,
                "created_at": emp.created_at.isoformat() if emp.created_at else None
            }
            for emp in recent_employees_query
        ]
        
        # Get recent attendance (last 5)
        recent_attendance_query = db.query(Attendance).join(Employee).order_by(
            Attendance.created_at.desc()
        ).limit(5).all()
        
        recent_attendance = [
            {
                "id": att.id,
                "employee_id": att.employee_id,
                "employee_name": att.employee.full_name if att.employee else f"Employee {att.employee_id}",
                "date": att.date.isoformat() if att.date else None,
                "status": att.status,
                "created_at": att.created_at.isoformat() if att.created_at else None
            }
            for att in recent_attendance_query
        ]
        
        # Get pending leave approvals count
        pending_leaves_count = db.query(func.count(Leave.id)).filter(
            Leave.status == "Pending"
        ).scalar() or 0
        
        return DashboardStatsResponse(
            total_employees=total_employees,
            total_attendance_records=total_attendance_records,
            total_present_today=total_present_today,
            total_absent_today=total_absent_today,
            average_attendance_rate=average_attendance_rate,
            employees_by_department=employees_by_department,
            this_week_summary=this_week_summary,
            recent_employees=recent_employees,
            recent_attendance=recent_attendance,
            pending_leaves=pending_leaves_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving dashboard stats: {str(e)}"
        )


@router.get(
    "/employee-summaries",
    response_model=List[EmployeeSummaryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get top employees by attendance rate",
    description="Get top 10 employees with best attendance rates"
)
def get_employee_summaries(
    db: Session = Depends(get_db)
):
    """
    Get top 10 employees with best attendance rates.
    
    Returns:
    - List of employees with attendance statistics sorted by attendance rate
    """
    try:
        summaries = AttendanceService.get_all_employees_summary(db)
        
        # Calculate attendance rate for each employee
        for summary in summaries:
            total_days = summary.get("total_days", 0)
            if total_days > 0:
                attendance_rate = (summary.get("total_present_days", 0) / total_days) * 100
            else:
                attendance_rate = 0.0
            summary["attendance_rate"] = round(attendance_rate, 2)
        
        # Sort by attendance rate (descending) and take top 10
        summaries.sort(key=lambda x: x.get("attendance_rate", 0), reverse=True)
        top_summaries = summaries[:10]
        
        # Convert to response models
        return [
            EmployeeSummaryResponse(
                employee_id=summary["employee_id"],
                employee_name=summary["employee_name"],
                employee_code=summary["employee_code"],
                department=summary["department"],
                total_present_days=summary["total_present_days"],
                total_absent_days=summary["total_absent_days"],
                total_days=summary["total_days"]
            )
            for summary in top_summaries
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving employee summaries: {str(e)}"
        )
