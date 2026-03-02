import './RecentActivity.css';

const RecentActivity = ({ recentEmployees, recentAttendance }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="recent-activity">
      <h3>Recent Activity</h3>
      
      <div className="activity-section">
        <h4>Recent Employees</h4>
        {!recentEmployees || recentEmployees.length === 0 ? (
          <div className="empty-state">
            <p>No recent employees</p>
          </div>
        ) : (
          <div className="activity-list">
            {recentEmployees.map((emp) => (
              <div key={emp.id} className="activity-item">
                <div className="activity-icon">👤</div>
                <div className="activity-content">
                  <div className="activity-title">{emp.full_name}</div>
                  <div className="activity-meta">
                    {emp.department} • {formatDate(emp.created_at)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="activity-section">
        <h4>Recent Attendance</h4>
        {!recentAttendance || recentAttendance.length === 0 ? (
          <div className="empty-state">
            <p>No recent attendance records</p>
          </div>
        ) : (
          <div className="activity-list">
            {recentAttendance.map((att) => (
              <div key={att.id} className="activity-item">
                <div className={`activity-icon ${att.status === 'Present' ? 'present' : 'absent'}`}>
                  {att.status === 'Present' ? '✅' : '❌'}
                </div>
                <div className="activity-content">
                  <div className="activity-title">{att.employee_name}</div>
                  <div className="activity-meta">
                    <span className={`status-badge ${att.status === 'Present' ? 'status-present' : 'status-absent'}`}>
                      {att.status}
                    </span>
                    {' • '}
                    {formatDate(att.date)} • {formatDateTime(att.created_at)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecentActivity;
