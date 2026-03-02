import { useState, useEffect } from 'react';
import { leaveAPI, employeeAPI } from '../services/api';
import ErrorAlert from './ErrorAlert';
import './LeaveForm.css';

const LeaveForm = ({ onLeaveCreated }) => {
  const [formData, setFormData] = useState({
    employee_id: '',
    leave_type: 'Annual',
    start_date: '',
    end_date: '',
    reason: '',
  });
  const [employees, setEmployees] = useState([]);
  const [leaveBalance, setLeaveBalance] = useState(null);
  const [calculatedDays, setCalculatedDays] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchEmployees();
  }, []);

  useEffect(() => {
    if (formData.employee_id && formData.start_date && formData.end_date) {
      calculateDays();
      if (formData.employee_id) {
        fetchLeaveBalance(formData.employee_id);
      }
    }
  }, [formData.start_date, formData.end_date, formData.employee_id]);

  const fetchEmployees = async () => {
    try {
      const response = await employeeAPI.getAll();
      setEmployees(response.data?.data || []);
    } catch (err) {
      setError('Failed to fetch employees');
    }
  };

  const fetchLeaveBalance = async (employeeId) => {
    try {
      const response = await leaveAPI.getBalance(employeeId);
      setLeaveBalance(response.data);
    } catch (err) {
      // Don't show error if balance fetch fails
    }
  };

  const calculateDays = () => {
    if (!formData.start_date || !formData.end_date) {
      setCalculatedDays(0);
      return;
    }

    const start = new Date(formData.start_date);
    const end = new Date(formData.end_date);

    if (start > end) {
      setCalculatedDays(0);
      return;
    }

    let days = 0;
    let current = new Date(start);
    while (current <= end) {
      const dayOfWeek = current.getDay();
      if (dayOfWeek !== 0 && dayOfWeek !== 6) { // Exclude weekends
        days++;
      }
      current.setDate(current.getDate() + 1);
    }
    setCalculatedDays(days);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await leaveAPI.create({
        ...formData,
        employee_id: parseInt(formData.employee_id)
      });
      setSuccess('Leave application submitted successfully!');
      setFormData({
        employee_id: '',
        leave_type: 'Annual',
        start_date: '',
        end_date: '',
        reason: '',
      });
      setCalculatedDays(0);
      setLeaveBalance(null);
      if (onLeaveCreated) {
        onLeaveCreated();
      }
      if (window.showToast) {
        window.showToast('Leave application submitted successfully!', 'success');
      }
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Failed to submit leave application';
      setError(errorMsg);
      if (window.showToast) {
        window.showToast(errorMsg, 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const getRemainingBalance = () => {
    if (!leaveBalance) return null;
    const type = formData.leave_type.toLowerCase();
    if (type === 'annual') return leaveBalance.annual_leave_remaining;
    if (type === 'sick') return leaveBalance.sick_leave_remaining;
    if (type === 'casual') return leaveBalance.casual_leave_remaining;
    if (type === 'emergency') return leaveBalance.emergency_leave_remaining;
    return null;
  };

  return (
    <div className="leave-form-container">
      <h2>Apply for Leave</h2>
      
      <ErrorAlert message={error} onClose={() => setError('')} />
      {success && (
        <div className="success-alert">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="leave-form">
        <div className="form-group">
          <label htmlFor="employee_id">Employee *</label>
          <select
            id="employee_id"
            name="employee_id"
            value={formData.employee_id}
            onChange={handleChange}
            required
          >
            <option value="">Select Employee</option>
            {employees.map(emp => (
              <option key={emp.id} value={emp.id}>
                {emp.employee_id} - {emp.full_name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="leave_type">Leave Type *</label>
          <select
            id="leave_type"
            name="leave_type"
            value={formData.leave_type}
            onChange={handleChange}
            required
          >
            <option value="Annual">Annual</option>
            <option value="Sick">Sick</option>
            <option value="Casual">Casual</option>
            <option value="Emergency">Emergency</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="start_date">Start Date *</label>
            <input
              type="date"
              id="start_date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              min={new Date().toISOString().split('T')[0]}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="end_date">End Date *</label>
            <input
              type="date"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              min={formData.start_date || new Date().toISOString().split('T')[0]}
              required
            />
          </div>
        </div>

        {calculatedDays > 0 && (
          <div className="days-info">
            <strong>Working Days: {calculatedDays}</strong>
            {leaveBalance && (
              <span className={`balance ${getRemainingBalance() >= calculatedDays ? 'sufficient' : 'insufficient'}`}>
                Remaining Balance: {getRemainingBalance() || 0} days
              </span>
            )}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="reason">Reason</label>
          <textarea
            id="reason"
            name="reason"
            value={formData.reason}
            onChange={handleChange}
            rows="4"
            placeholder="Enter reason for leave (optional)"
            maxLength={500}
          />
        </div>

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Leave Application'}
        </button>
      </form>
    </div>
  );
};

export default LeaveForm;
