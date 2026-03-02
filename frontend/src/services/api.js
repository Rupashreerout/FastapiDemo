/**
 * API service layer for HRMS Lite
 * Centralized axios instance with error handling
 */
import axios from 'axios';

// Get API base URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

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
      const [employeesRes, attendanceRes] = await Promise.all([
        api.get('/employees'),
        api.get('/attendance'),
      ]);
      
      const employees = employeesRes.data?.data || [];
      const attendanceRecords = attendanceRes.data?.data || [];
      
      // Calculate today's present count
      const today = new Date().toISOString().split('T')[0];
      const todayPresent = attendanceRecords.filter(
        (record) => record.date === today && record.status === 'Present'
      ).length;
      
      return {
        totalEmployees: employees.length,
        totalAttendanceRecords: attendanceRecords.length,
        totalPresentToday: todayPresent,
      };
    } catch (error) {
      throw error;
    }
  },
};

export default api;
