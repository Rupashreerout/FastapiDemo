import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import StatCard from './StatCard';
import EmployeeSummaryTable from './EmployeeSummaryTable';
import DepartmentStats from './DepartmentStats';
import RecentActivity from './RecentActivity';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_employees: 0,
    total_attendance_records: 0,
    total_present_today: 0,
    total_absent_today: 0,
    average_attendance_rate: 0,
    employees_by_department: {},
    this_week_summary: {},
    recent_employees: [],
    recent_attendance: [],
  });
  const [employeeSummaries, setEmployeeSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingSummaries, setLoadingSummaries] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');

    try {
      const [dashboardStats, summaries] = await Promise.all([
        dashboardAPI.getStats(),
        dashboardAPI.getEmployeeSummaries().catch(() => []), // Don't fail if summaries fail
      ]);
      
      setStats(dashboardStats);
      setEmployeeSummaries(summaries || []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getAttendanceRateColor = (rate) => {
    if (rate >= 80) return 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    if (rate >= 50) return 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    return 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
  };

  if (loading) {
    return <Loader />;
  }

  const presentPercentage = stats.total_employees > 0
    ? ((stats.total_present_today / stats.total_employees) * 100).toFixed(1)
    : 0;

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>

      <ErrorAlert message={error} onClose={() => setError('')} />

      {/* Top Section: Stat Cards */}
      <div className="stats-grid">
        <StatCard
          icon="👥"
          label="Total Employees"
          value={stats.total_employees || 0}
        />
        <StatCard
          icon="✅"
          label="Present Today"
          value={stats.total_present_today || 0}
          suffix={`(${presentPercentage}%)`}
        />
        <StatCard
          icon="❌"
          label="Absent Today"
          value={stats.total_absent_today || 0}
        />
        <StatCard
          icon="📊"
          label="Average Attendance Rate"
          value={stats.average_attendance_rate?.toFixed(1) || 0}
          suffix="%"
          gradient={getAttendanceRateColor(stats.average_attendance_rate || 0)}
        />
        <StatCard
          icon="📋"
          label="Total Records"
          value={stats.total_attendance_records || 0}
        />
      </div>

      {/* Middle Section: Two Columns */}
      <div className="dashboard-middle">
        <div className="dashboard-column left">
          <EmployeeSummaryTable summaries={employeeSummaries} loading={loadingSummaries} />
        </div>
        <div className="dashboard-column right">
          <DepartmentStats
            departments={stats.employees_by_department || {}}
            thisWeekSummary={stats.this_week_summary || {}}
          />
          <RecentActivity
            recentEmployees={stats.recent_employees || []}
            recentAttendance={stats.recent_attendance || []}
          />
        </div>
      </div>

      {/* Bottom Section: Quick Actions */}
      <div className="dashboard-section">
        <h2>Quick Actions</h2>
        <div className="quick-actions">
          <a href="/employees" className="action-card">
            <span className="action-icon">➕</span>
            <span>Add Employee</span>
          </a>
          <a href="/attendance" className="action-card">
            <span className="action-icon">📝</span>
            <span>Mark Attendance</span>
          </a>
          <a href="/employees" className="action-card">
            <span className="action-icon">👥</span>
            <span>View Employees</span>
          </a>
          <a href="/attendance" className="action-card">
            <span className="action-icon">📋</span>
            <span>View Attendance</span>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
