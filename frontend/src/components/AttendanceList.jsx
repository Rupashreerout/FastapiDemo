import { useState, useEffect, useMemo } from 'react';
import { attendanceAPI, employeeAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import './AttendanceList.css';

const AttendanceList = () => {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDate, setFilterDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, [selectedEmployee]);

  const fetchData = async () => {
    setLoading(true);
    setError('');

    try {
      const [employeesRes, attendanceRes] = await Promise.all([
        employeeAPI.getAll(),
        selectedEmployee === 'all'
          ? attendanceAPI.getAll()
          : attendanceAPI.getByEmployeeId(parseInt(selectedEmployee)),
      ]);

      const employeesData = employeesRes.data?.data || [];
      const attendanceData = attendanceRes.data?.data || [];

      setEmployees(employeesData);
      setAttendanceRecords(attendanceData);
    } catch (err) {
      setError(err.message || 'Failed to fetch attendance records');
    } finally {
      setLoading(false);
    }
  };

  const getEmployeeName = (employeeId) => {
    const employee = employees.find((emp) => emp.id === employeeId);
    return employee
      ? `${employee.employee_id} - ${employee.full_name}`
      : `Employee ID: ${employeeId}`;
  };

  // Filter attendance records
  const filteredRecords = useMemo(() => {
    let filtered = attendanceRecords;

    // Filter by date
    if (filterDate) {
      filtered = filtered.filter(record => record.date === filterDate);
    }

    // Filter by search query (employee name)
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(record => {
        const employee = employees.find(emp => emp.id === record.employee_id);
        if (!employee) return false;
        return employee.full_name?.toLowerCase().includes(query) ||
               employee.employee_id?.toLowerCase().includes(query);
      });
    }

    return filtered;
  }, [attendanceRecords, filterDate, searchQuery, employees]);

  // Group attendance by employee
  const groupedAttendance = useMemo(() => {
    return filteredRecords.reduce((acc, record) => {
      const empId = record.employee_id;
      if (!acc[empId]) {
        acc[empId] = [];
      }
      acc[empId].push(record);
      return acc;
    }, {});
  }, [filteredRecords]);

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="attendance-list-container">
      <div className="attendance-list-header">
        <h2>Attendance Records</h2>
        <div className="header-controls">
          <select
            value={selectedEmployee}
            onChange={(e) => setSelectedEmployee(e.target.value)}
            className="employee-filter"
          >
            <option value="all">All Employees</option>
            {employees.map((employee) => (
              <option key={employee.id} value={employee.id}>
                {employee.employee_id} - {employee.full_name}
              </option>
            ))}
          </select>
          <span className="attendance-count">
            {filteredRecords.length} of {attendanceRecords.length} record(s)
          </span>
        </div>
      </div>

      <ErrorAlert message={error} onClose={() => setError('')} />

      {/* Filters */}
      <div className="filters-container">
        <input
          type="text"
          placeholder="Search by employee name..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <input
          type="date"
          value={filterDate}
          onChange={(e) => setFilterDate(e.target.value)}
          className="date-filter"
        />
        {filterDate && (
          <button
            onClick={() => setFilterDate('')}
            className="clear-filter-btn"
          >
            Clear Date
          </button>
        )}
      </div>

      {attendanceRecords.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <p>
            {selectedEmployee === 'all'
              ? 'No attendance records found.'
              : 'No attendance records found for this employee.'}
          </p>
        </div>
      ) : filteredRecords.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <p>No attendance records found matching your filters.</p>
          <button
            className="empty-action-btn"
            onClick={() => {
              setSearchQuery('');
              setFilterDate('');
            }}
          >
            Clear Filters
          </button>
        </div>
      ) : selectedEmployee === 'all' ? (
        // Grouped view for all employees
        <div className="grouped-attendance">
          {Object.entries(groupedAttendance).map(([employeeId, records]) => (
            <div key={employeeId} className="employee-attendance-group">
              <h3 className="employee-name">
                {getEmployeeName(parseInt(employeeId))}
              </h3>
              <div className="table-container">
                <table className="attendance-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Marked At</th>
                    </tr>
                  </thead>
                  <tbody>
                    {records
                      .sort((a, b) => new Date(b.date) - new Date(a.date))
                      .map((record) => (
                        <tr key={record.id}>
                          <td>
                            {new Date(record.date).toLocaleDateString()}
                          </td>
                          <td>
                            <span
                              className={`status-badge ${
                                record.status === 'Present'
                                  ? 'status-present'
                                  : 'status-absent'
                              }`}
                            >
                              {record.status}
                            </span>
                          </td>
                          <td>
                            {new Date(record.created_at).toLocaleString()}
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      ) : (
        // Simple table view for single employee
        <div className="table-container">
          <table className="attendance-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Status</th>
                <th>Marked At</th>
              </tr>
            </thead>
            <tbody>
              {filteredRecords
                .sort((a, b) => new Date(b.date) - new Date(a.date))
                .map((record) => (
                  <tr key={record.id}>
                    <td>{new Date(record.date).toLocaleDateString()}</td>
                    <td>
                      <span
                        className={`status-badge ${
                          record.status === 'Present'
                            ? 'status-present'
                            : 'status-absent'
                        }`}
                      >
                        {record.status}
                      </span>
                    </td>
                    <td>
                      {new Date(record.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AttendanceList;
