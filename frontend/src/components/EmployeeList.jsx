import { useState, useEffect } from 'react';
import { employeeAPI } from '../services/api';
import Loader from './Loader';
import ErrorAlert from './ErrorAlert';
import EditEmployeeModal from './EditEmployeeModal';
import './EmployeeList.css';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [editingEmployee, setEditingEmployee] = useState(null);

  const fetchEmployees = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await employeeAPI.getAll();
      const employeesData = response.data?.data || [];
      setEmployees(employeesData);
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

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="employee-list-container">
      <div className="employee-list-header">
        <h2>Employees</h2>
        <span className="employee-count">{employees.length} employee(s)</span>
      </div>

      <ErrorAlert message={error} onClose={() => setError('')} />

      {employees.length === 0 ? (
        <div className="empty-state">
          <p>No employees found. Add your first employee to get started.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="employee-table">
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Full Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((employee) => (
                <tr key={employee.id}>
                  <td>{employee.employee_id}</td>
                  <td>{employee.full_name}</td>
                  <td>{employee.email}</td>
                  <td>{employee.department}</td>
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
              ))}
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
