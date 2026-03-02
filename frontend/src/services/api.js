/**
 * API service layer for HRMS Lite
 * Centralized axios instance with error handling
 */
import axios from 'axios';

// API base URL configuration
// For production deployment, use the deployed URL
const API_BASE_URL = 'https://fastapidemo-zshy.onrender.com/api';

// For local development, use localhost
// const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (optional - for adding auth tokens, etc.)
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      // Format error message
      let errorMessage = 'An error occurred';
      
      if (data?.message) {
        errorMessage = data.message;
      } else if (data?.detail) {
        errorMessage = data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      return Promise.reject({
        status,
        message: errorMessage,
        data: data || {},
      });
    } else if (error.request) {
      // Request made but no response received
      return Promise.reject({
        status: 0,
        message: 'Network error. Please check your connection.',
      });
    } else {
      // Something else happened
      return Promise.reject({
        status: 0,
        message: error.message || 'An unexpected error occurred',
      });
    }
  }
);

// Employee API methods
export const employeeAPI = {
  // Get all employees
  getAll: () => api.get('/employees'),
  
  // Get employee by ID
  getById: (id) => api.get(`/employees/${id}`),
  
  // Create employee
  create: (employeeData) => api.post('/employees', employeeData),
  
  // Update employee
  update: (id, employeeData) => api.put(`/employees/${id}`, employeeData),
  
  // Delete employee
  delete: (id) => api.delete(`/employees/${id}`),
};

// Attendance API methods
export const attendanceAPI = {
  // Get all attendance records
  getAll: () => api.get('/attendance'),
  
  // Get attendance by employee ID
  getByEmployeeId: (employeeId) => api.get(`/attendance/employee/${employeeId}`),
  
  // Get attendance summary for employee
  getSummary: (employeeId) => api.get(`/attendance/employee/${employeeId}/summary`),
  
  // Create attendance record
  create: (attendanceData) => api.post('/attendance', attendanceData),
};

// Dashboard API methods
export const dashboardAPI = {
  // Get dashboard stats
  getStats: async () => {
    try {
      const response = await api.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // Get employee summaries (top 10 by attendance rate)
  getEmployeeSummaries: async () => {
    try {
      const response = await api.get('/dashboard/employee-summaries');
      return response.data || [];
    } catch (error) {
      throw error;
    }
  },
};

// Leave API methods
export const leaveAPI = {
  // Get all leaves
  getAll: (params) => api.get('/leaves', { params }),
  
  // Get leave by ID
  getById: (id) => api.get(`/leaves/${id}`),
  
  // Create leave
  create: (leaveData) => api.post('/leaves', leaveData),
  
  // Update leave status
  updateStatus: (id, status, reviewedBy) => api.put(`/leaves/${id}/status`, { status, reviewed_by: reviewedBy }),
  
  // Get employee's leaves
  getByEmployeeId: (employeeId) => api.get(`/leaves/employee/${employeeId}`),
  
  // Get employee leave balance
  getBalance: (employeeId) => api.get(`/leaves/employee/${employeeId}/balance`),
  
  // Get leave statistics
  getStatistics: () => api.get('/leaves/statistics'),
};

export default api;
