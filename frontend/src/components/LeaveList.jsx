import { useState, useEffect } from 'react';
import { leaveAPI, employeeAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import './LeaveList.css';

const LeaveList = ({ refreshKey }) => {
  const [leaves, setLeaves] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    status: '',
    employee_id: '',
  });

  useEffect(() => {
    fetchData();
  }, [refreshKey, filters]);

  const fetchData = async () => {
    setLoading(true);
    setError('');

    try {
      const [leavesRes, employeesRes] = await Promise.all([
        leaveAPI.getAll(filters).catch(err => {
          // If leaves table doesn't exist yet, return empty array
          if (err.response?.status === 500 || err.message?.includes('relation') || err.message?.includes('does not exist')) {
            console.warn('Leaves table may not exist yet. Run migration: alembic upgrade head');
            return { data: { data: [] } };
          }
          throw err;
        }),
        employeeAPI.getAll(),
      ]);

      setLeaves(leavesRes.data?.data || leavesRes.data || []);
      setEmployees(employeesRes.data?.data || []);
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Failed to fetch leave records';
      setError(errorMsg);
      console.error('Error fetching leaves:', err);
      // Set empty arrays to prevent blank page
      setLeaves([]);
      setEmployees([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (leaveId, newStatus) => {
    if (!window.confirm(`Are you sure you want to ${newStatus.toLowerCase()} this leave?`)) {
      return;
    }

    try {
      await leaveAPI.updateStatus(leaveId, newStatus, null); // TODO: Get current user ID
      if (window.showToast) {
        window.showToast(`Leave ${newStatus.toLowerCase()} successfully!`, 'success');
      }
      fetchData();
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Failed to update leave status';
      if (window.showToast) {
        window.showToast(errorMsg, 'error');
      }
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'Approved':
        return 'status-approved';
      case 'Rejected':
        return 'status-rejected';
      default:
        return 'status-pending';
    }
  };

  return (
    <div className="leave-list-container">
      {loading && <Loader />}
      <div className="leave-list-header">
        <h2>Leave Applications</h2>
        <div className="header-controls">
          <select
            value={filters.status}
            onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            className="filter-select"
          >
            <option value="">All Status</option>
            <option value="Pending">Pending</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
          </select>
          <select
            value={filters.employee_id}
            onChange={(e) => setFilters(prev => ({ ...prev, employee_id: e.target.value }))}
            className="filter-select"
          >
            <option value="">All Employees</option>
            {employees.map(emp => (
              <option key={emp.id} value={emp.id}>
                {emp.employee_id} - {emp.full_name}
              </option>
            ))}
          </select>
          <span className="leave-count">{leaves.length} leave(s)</span>
        </div>
      </div>

      <ErrorAlert message={error} onClose={() => setError('')} />

      {!loading && leaves.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <p>No leave applications found.</p>
          {error && error.includes('relation') && (
            <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
              Note: Please run database migration: <code>alembic upgrade head</code>
            </p>
          )}
        </div>
      ) : !loading ? (
        <div className="table-container">
          <table className="leave-table">
            <thead>
              <tr>
                <th>Employee</th>
                <th>Leave Type</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Days</th>
                <th>Status</th>
                <th>Applied At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {leaves.map((leave) => (
                <tr key={leave.id}>
                  <td>{leave.employee_name || `Employee ${leave.employee_id}`}</td>
                  <td>{leave.leave_type}</td>
                  <td>{new Date(leave.start_date).toLocaleDateString()}</td>
                  <td>{new Date(leave.end_date).toLocaleDateString()}</td>
                  <td>{leave.days}</td>
                  <td>
                    <span className={`status-badge ${getStatusBadgeClass(leave.status)}`}>
                      {leave.status}
                    </span>
                  </td>
                  <td>{new Date(leave.applied_at).toLocaleDateString()}</td>
                  <td>
                    {leave.status === 'Pending' && (
                      <div className="action-buttons">
                        <button
                          className="btn-approve"
                          onClick={() => handleStatusUpdate(leave.id, 'Approved')}
                        >
                          Approve
                        </button>
                        <button
                          className="btn-reject"
                          onClick={() => handleStatusUpdate(leave.id, 'Rejected')}
                        >
                          Reject
                        </button>
                      </div>
                    )}
                    {leave.status !== 'Pending' && leave.reviewer_name && (
                      <span className="reviewed-by">Reviewed by: {leave.reviewer_name}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
};

export default LeaveList;
