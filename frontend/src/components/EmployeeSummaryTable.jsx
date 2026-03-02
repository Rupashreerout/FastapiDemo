import './EmployeeSummaryTable.css';

const EmployeeSummaryTable = ({ summaries, loading }) => {
  const getAttendanceRateColor = (rate) => {
    if (rate >= 80) return 'rate-high';
    if (rate >= 50) return 'rate-medium';
    return 'rate-low';
  };

  const calculateRate = (present, absent) => {
    const total = present + absent;
    if (total === 0) return 0;
    return ((present / total) * 100).toFixed(1);
  };

  if (loading) {
    return (
      <div className="employee-summary-table">
        <h3>Top Employees by Attendance</h3>
        <div className="loading-skeleton">
          <div className="skeleton-row"></div>
          <div className="skeleton-row"></div>
          <div className="skeleton-row"></div>
        </div>
      </div>
    );
  }

  if (!summaries || summaries.length === 0) {
    return (
      <div className="employee-summary-table">
        <h3>Top Employees by Attendance</h3>
        <div className="empty-state">
          <p>No employee data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="employee-summary-table">
      <h3>Top Employees by Attendance</h3>
      <div className="table-container">
        <table className="summary-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Department</th>
              <th>Present</th>
              <th>Absent</th>
              <th>Rate</th>
            </tr>
          </thead>
          <tbody>
            {summaries.map((summary) => {
              const rate = calculateRate(
                summary.total_present_days || 0,
                summary.total_absent_days || 0
              );
              return (
                <tr key={summary.employee_id}>
                  <td className="employee-name">{summary.employee_name}</td>
                  <td>{summary.department}</td>
                  <td className="present-count">{summary.total_present_days || 0}</td>
                  <td className="absent-count">{summary.total_absent_days || 0}</td>
                  <td>
                    <span className={`attendance-rate ${getAttendanceRateColor(parseFloat(rate))}`}>
                      {rate}%
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EmployeeSummaryTable;
