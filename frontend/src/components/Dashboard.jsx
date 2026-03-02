import { useState, useEffect } from 'react';
import { dashboardAPI, attendanceAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    totalAttendanceRecords: 0,
    totalPresentToday: 0,
  });
  const [employeeSummaries, setEmployeeSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');

    try {
      const dashboardStats = await dashboardAPI.getStats();
      setStats(dashboardStats);
      setEmployeeSummaries([]);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>

      <ErrorAlert message={error} onClose={() => setError('')} />

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Total Employees</h3>
            <p className="stat-value">{stats.totalEmployees}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Total Attendance Records</h3>
            <p className="stat-value">{stats.totalAttendanceRecords}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Present Today</h3>
            <p className="stat-value">{stats.totalPresentToday}</p>
          </div>
        </div>
      </div>

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
