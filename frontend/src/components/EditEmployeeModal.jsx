import { useState, useEffect } from 'react';
import { employeeAPI } from '../services/api';
import ErrorAlert from './ErrorAlert';
import SuccessAlert from './SuccessAlert';
import './EditEmployeeModal.css';

const EditEmployeeModal = ({ employee, onClose, onEmployeeUpdated }) => {
  const [formData, setFormData] = useState({
    employee_id: '',
    full_name: '',
    email: '',
    department: '',
  });
  
  const [errors, setErrors] = useState({});
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (employee) {
      setFormData({
        employee_id: employee.employee_id || '',
        full_name: employee.full_name || '',
        email: employee.email || '',
        department: employee.department || '',
      });
    }
  }, [employee]);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    const newErrors = {};

    if (formData.employee_id && !formData.employee_id.trim()) {
      newErrors.employee_id = 'Employee ID cannot be empty';
    }

    if (formData.full_name && !formData.full_name.trim()) {
      newErrors.full_name = 'Full name cannot be empty';
    }

    if (formData.email && !formData.email.trim()) {
      newErrors.email = 'Email cannot be empty';
    } else if (formData.email && !validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (formData.department && !formData.department.trim()) {
      newErrors.department = 'Department cannot be empty';
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
      // Only send fields that have values
      const updateData = {};
      if (formData.employee_id) updateData.employee_id = formData.employee_id;
      if (formData.full_name) updateData.full_name = formData.full_name;
      if (formData.email) updateData.email = formData.email;
      if (formData.department) updateData.department = formData.department;

      const response = await employeeAPI.update(employee.id, updateData);
      
      if (response.data) {
        setSuccessMessage('Employee updated successfully!');
        
        if (onEmployeeUpdated) {
          setTimeout(() => {
            onEmployeeUpdated();
            onClose();
            setSuccessMessage('');
          }, 1500);
        }
      }
    } catch (error) {
      setErrorMessage(
        error.message || 'Failed to update employee. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!employee) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit Employee</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <ErrorAlert message={errorMessage} onClose={() => setErrorMessage('')} />
        <SuccessAlert message={successMessage} onClose={() => setSuccessMessage('')} />

        <form onSubmit={handleSubmit} className="edit-employee-form">
          <div className="form-group">
            <label htmlFor="edit_employee_id">Employee ID</label>
            <input
              type="text"
              id="edit_employee_id"
              name="employee_id"
              value={formData.employee_id}
              onChange={handleChange}
              className={errors.employee_id ? 'error' : ''}
              placeholder="e.g., EMP001"
            />
            {errors.employee_id && (
              <span className="field-error">{errors.employee_id}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="edit_full_name">Full Name</label>
            <input
              type="text"
              id="edit_full_name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              className={errors.full_name ? 'error' : ''}
              placeholder="John Doe"
            />
            {errors.full_name && (
              <span className="field-error">{errors.full_name}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="edit_email">Email</label>
            <input
              type="email"
              id="edit_email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="john.doe@example.com"
            />
            {errors.email && (
              <span className="field-error">{errors.email}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="edit_department">Department</label>
            <input
              type="text"
              id="edit_department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              className={errors.department ? 'error' : ''}
              placeholder="Engineering"
            />
            {errors.department && (
              <span className="field-error">{errors.department}</span>
            )}
          </div>

          <div className="form-actions">
            <button type="submit" disabled={isSubmitting} className="btn-primary">
              {isSubmitting ? 'Updating...' : 'Update Employee'}
            </button>
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditEmployeeModal;
