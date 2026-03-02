import { useState } from 'react';
import AttendanceForm from '../components/AttendanceForm';
import AttendanceList from '../components/AttendanceList';
import './AttendancePage.css';

const AttendancePage = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleAttendanceCreated = () => {
    // Trigger refresh of attendance list
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="attendance-page">
      <AttendanceForm onAttendanceCreated={handleAttendanceCreated} />
      <AttendanceList key={refreshKey} />
    </div>
  );
};

export default AttendancePage;
