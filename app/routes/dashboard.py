"""
Dashboard API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database import get_db
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.schemas.dashboard import DashboardStatsResponse

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
        
        return DashboardStatsResponse(
            total_employees=total_employees,
            total_attendance_records=total_attendance_records,
            total_present_today=total_present_today,
            total_absent_today=total_absent_today
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving dashboard stats: {str(e)}"
        )
