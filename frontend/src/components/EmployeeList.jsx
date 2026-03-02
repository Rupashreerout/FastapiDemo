import { useState, useEffect, useMemo } from 'react';
import { employeeAPI, attendanceAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import EditEmployeeModal from './EditEmployeeModal';
import './EmployeeList.css';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);
  const [attendanceSummaries, setAttendanceSummaries] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [editingEmployee, setEditingEmployee] = useState(null);

  const fetchEmployees = async () => {
    setLoading(true);
    setError('');
    
    try {
      const employeesRes = await employeeAPI.getAll();
      const employeesData = employeesRes.data?.data || [];
      setEmployees(employeesData);
      
      // Fetch attendance summaries
      try {
        const summariesRes = await fetch('https://fastapidemo-zshy.onrender.com/api/attendance/employees/summary')
          .then(res => res.json())
          .catch(() => []);
        setAttendanceSummaries(summariesRes || []);
      } catch (summaryErr) {
        // Don't fail if summaries can't be loaded
        setAttendanceSummaries([]);
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch employees');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleDelete = async (id, employeeId) => {
    if (deleteConfirm !== id) {
      setDeleteConfirm(id);
      return;
    }

    try {
      await employeeAPI.delete(id);
      setDeleteConfirm(null);
      fetchEmployees(); // Refresh list
    } catch (err) {
      setError(err.message || 'Failed to delete employee');
      setDeleteConfirm(null);
    }
  };

  const cancelDelete = () => {
    setDeleteConfirm(null);
  };

  const getAttendanceRate = (employeeId) => {
    const summary = attendanceSummaries.find(s => s.employee_id === employeeId);
    if (!summary || summary.total_days === 0) return null;
    return ((summary.total_present_days / summary.total_days) * 100).toFixed(1);
  };

  const getAttendanceRateColor = (rate) => {
    if (!rate) return '';
    const numRate = parseFloat(rate);
    if (numRate >= 80) return 'rate-high';
    if (numRate >= 50) return 'rate-medium';
    return 'rate-low';
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedEmployees = useMemo(() => {
    let filtered = employees;

    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(emp =>
        emp.full_name?.toLowerCase().includes(query) ||
        emp.email?.toLowerCase().includes(query) ||
        emp.employee_id?.toLowerCase().includes(query) ||
        emp.department?.toLowerCase().includes(query)
      );
    }

    // Apply sorting
    if (sortField) {
      filtered = [...filtered].sort((a, b) => {
        let aVal = a[sortField];
        let bVal = b[sortField];

        if (sortField === 'created_at') {
          aVal = new Date(aVal);
          bVal = new Date(bVal);
        } else if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase();
          bVal = bVal.toLowerCase();
        }

        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return filtered;
  }, [employees, searchQuery, sortField, sortDirection]);

  const getSortIcon = (field) => {
    if (sortField !== field) return '↕️';
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="employee-list-container">
      <div className="employee-list-header">
        <h2>Employees</h2>
        <span className="employee-count">
          {filteredAndSortedEmployees.length} of {employees.length} employee(s)
        </span>
      </div>

      <ErrorAlert message={error} onClose={() => setError('')} />

      {/* Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by name, email, employee ID, or department..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </div>

      {employees.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">👥</div>
          <p>No employees found. Add your first employee to get started.</p>
          <a href="/employees" className="empty-action-btn">Add Employee</a>
        </div>
      ) : filteredAndSortedEmployees.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <p>No employees found matching your search.</p>
          <button
            className="empty-action-btn"
            onClick={() => setSearchQuery('')}
          >
            Clear Search
          </button>
        </div>
      ) : (
        <div className="table-container">
          <table className="employee-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('employee_id')} className="sortable">
                  Employee ID {getSortIcon('employee_id')}
                </th>
                <th onClick={() => handleSort('full_name')} className="sortable">
                  Full Name {getSortIcon('full_name')}
                </th>
                <th onClick={() => handleSort('email')} className="sortable">
                  Email {getSortIcon('email')}
                </th>
                <th onClick={() => handleSort('department')} className="sortable">
                  Department {getSortIcon('department')}
                </th>
                <th>Attendance Rate</th>
                <th onClick={() => handleSort('created_at')} className="sortable">
                  Created At {getSortIcon('created_at')}
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAndSortedEmployees.map((employee) => {
                const attendanceRate = getAttendanceRate(employee.id);
                return (
                  <tr key={employee.id}>
                    <td>{employee.employee_id}</td>
                    <td>{employee.full_name}</td>
                    <td>{employee.email}</td>
                    <td>{employee.department}</td>
                    <td>
                      {attendanceRate ? (
                        <span className={`attendance-rate ${getAttendanceRateColor(attendanceRate)}`}>
                          {attendanceRate}%
                        </span>
                      ) : (
                        <span className="attendance-rate no-data">N/A</span>
                      )}
                    </td>
                    <td>
                      {new Date(employee.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      {deleteConfirm === employee.id ? (
                        <div className="delete-confirm">
                          <button
                            className="btn-confirm"
                            onClick={() => handleDelete(employee.id, employee.employee_id)}
                          >
                            Confirm
                          </button>
                          <button
                            className="btn-cancel"
                            onClick={cancelDelete}
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <div className="action-buttons">
                          <button
                            className="btn-edit"
                            onClick={() => setEditingEmployee(employee)}
                            title="Edit employee"
                          >
                            ✏️ Edit
                          </button>
                          <button
                            className="btn-delete"
                            onClick={() => handleDelete(employee.id, employee.employee_id)}
                            title="Delete employee"
                          >
                            🗑️ Delete
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {editingEmployee && (
        <EditEmployeeModal
          employee={editingEmployee}
          onClose={() => setEditingEmployee(null)}
          onEmployeeUpdated={fetchEmployees}
        />
      )}
    </div>
  );
};

export default EmployeeList;
