import './DepartmentStats.css';

const DepartmentStats = ({ departments, thisWeekSummary }) => {
  if (!departments || Object.keys(departments).length === 0) {
    return (
      <div className="department-stats">
        <h3>Department Breakdown</h3>
        <div className="empty-state">
          <p>No department data available</p>
        </div>
      </div>
    );
  }

  const totalEmployees = Object.values(departments).reduce((sum, count) => sum + count, 0);

  return (
    <div className="department-stats">
      <h3>Department Breakdown</h3>
      <div className="department-list">
        {Object.entries(departments).map(([dept, count]) => {
          const percentage = totalEmployees > 0 ? ((count / totalEmployees) * 100).toFixed(1) : 0;
          return (
            <div key={dept} className="department-item">
              <div className="department-header">
                <span className="department-name">{dept}</span>
                <span className="department-count">{count} employees</span>
              </div>
              <div className="department-bar">
                <div
                  className="department-bar-fill"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
              <span className="department-percentage">{percentage}%</span>
            </div>
          );
        })}
      </div>
      
      {thisWeekSummary && (
        <div className="week-summary">
          <h4>This Week Summary</h4>
          <div className="week-stats">
            <div className="week-stat present">
              <span className="week-label">Present</span>
              <span className="week-value">{thisWeekSummary.present || 0}</span>
            </div>
            <div className="week-stat absent">
              <span className="week-label">Absent</span>
              <span className="week-value">{thisWeekSummary.absent || 0}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DepartmentStats;
