import { useState } from 'react';
import { employeeAPI } from '../services/api';
import ErrorAlert from './ErrorAlert';
import SuccessAlert from './SuccessAlert';
import './EmployeeForm.css';

const EmployeeForm = ({ onEmployeeCreated, onCancel }) => {
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

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.employee_id.trim()) {
      newErrors.employee_id = 'Employee ID is required';
    }

    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Full name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.department.trim()) {
      newErrors.department = 'Department is required';
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
    // Clear error for this field when user starts typing
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
      const response = await employeeAPI.create(formData);
      
      if (response.data) {
        setSuccessMessage('Employee created successfully!');
        setFormData({
          employee_id: '',
          full_name: '',
          email: '',
          department: '',
        });
        
        // Callback to refresh employee list
        if (onEmployeeCreated) {
          setTimeout(() => {
            onEmployeeCreated();
            setSuccessMessage('');
          }, 1500);
        }
      }
    } catch (error) {
      setErrorMessage(
        error.message || 'Failed to create employee. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="employee-form-container">
      <h2>Add New Employee</h2>
      
      <ErrorAlert message={errorMessage} onClose={() => setErrorMessage('')} />
      <SuccessAlert message={successMessage} onClose={() => setSuccessMessage('')} />

      <form onSubmit={handleSubmit} className="employee-form">
        <div className="form-group">
          <label htmlFor="employee_id">
            Employee ID <span className="required">*</span>
          </label>
          <input
            type="text"
            id="employee_id"
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
          <label htmlFor="full_name">
            Full Name <span className="required">*</span>
          </label>
          <input
            type="text"
            id="full_name"
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
          <label htmlFor="email">
            Email <span className="required">*</span>
          </label>
          <input
            type="email"
            id="email"
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
          <label htmlFor="department">
            Department <span className="required">*</span>
          </label>
          <input
            type="text"
            id="department"
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
            {isSubmitting ? 'Creating...' : 'Create Employee'}
          </button>
          {onCancel && (
            <button type="button" onClick={onCancel} className="btn-secondary">
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default EmployeeForm;
