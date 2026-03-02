import { useState, useEffect } from 'react';
import { attendanceAPI, employeeAPI } from '../services/api';
import ErrorAlert from './ErrorAlert';
import SuccessAlert from './SuccessAlert';
import './AttendanceForm.css';

const AttendanceForm = ({ onAttendanceCreated }) => {
  const [formData, setFormData] = useState({
    employee_id: '',
    date: new Date().toISOString().split('T')[0],
    status: 'Present',
  });
  
  const [employees, setEmployees] = useState([]);
  const [errors, setErrors] = useState({});
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadingEmployees, setLoadingEmployees] = useState(true);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await employeeAPI.getAll();
        const employeesData = response.data?.data || [];
        setEmployees(employeesData);
      } catch (err) {
        setErrorMessage('Failed to load employees');
      } finally {
        setLoadingEmployees(false);
      }
    };

    fetchEmployees();
  }, []);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.employee_id) {
      newErrors.employee_id = 'Please select an employee';
    }

    if (!formData.date) {
      newErrors.date = 'Date is required';
    }

    if (!formData.status) {
      newErrors.status = 'Status is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const attendanceData = {
        employee_id: parseInt(formData.employee_id),
        date: formData.date,
        status: formData.status,
      };

      const response = await attendanceAPI.create(attendanceData);
      
      if (response.data) {
        setSuccessMessage('Attendance marked successfully!');
        setFormData({
          employee_id: '',
          date: new Date().toISOString().split('T')[0],
          status: 'Present',
        });
        
        if (onAttendanceCreated) {
          setTimeout(() => {
            onAttendanceCreated();
            setSuccessMessage('');
          }, 1500);
        }
      }
    } catch (error) {
      setErrorMessage(
        error.message || 'Failed to mark attendance. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loadingEmployees) {
    return <div className="loading">Loading employees...</div>;
  }

  return (
    <div className="attendance-form-container">
      <h2>Mark Attendance</h2>
      
      <ErrorAlert message={errorMessage} onClose={() => setErrorMessage('')} />
      <SuccessAlert message={successMessage} onClose={() => setSuccessMessage('')} />

      <form onSubmit={handleSubmit} className="attendance-form">
        <div className="form-group">
          <label htmlFor="employee_id">
            Employee <span className="required">*</span>
          </label>
          <select
            id="employee_id"
            name="employee_id"
            value={formData.employee_id}
            onChange={handleChange}
            className={errors.employee_id ? 'error' : ''}
          >
            <option value="">Select an employee</option>
            {employees.map((employee) => (
              <option key={employee.id} value={employee.id}>
                {employee.employee_id} - {employee.full_name} ({employee.department})
              </option>
            ))}
          </select>
          {errors.employee_id && (
            <span className="field-error">{errors.employee_id}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="date">
            Date <span className="required">*</span>
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className={errors.date ? 'error' : ''}
            max={new Date().toISOString().split('T')[0]}
          />
          {errors.date && (
            <span className="field-error">{errors.date}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="status">
            Status <span className="required">*</span>
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className={errors.status ? 'error' : ''}
          >
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
          {errors.status && (
            <span className="field-error">{errors.status}</span>
          )}
        </div>

        <div className="form-actions">
          <button type="submit" disabled={isSubmitting} className="btn-primary">
            {isSubmitting ? 'Marking...' : 'Mark Attendance'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AttendanceForm;
