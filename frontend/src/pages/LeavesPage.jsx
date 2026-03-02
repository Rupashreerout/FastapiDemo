import { useState } from 'react';
import LeaveForm from '../components/LeaveForm';
import LeaveList from '../components/LeaveList';
import './LeavesPage.css';

const LeavesPage = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleLeaveCreated = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="leaves-page">
      <LeaveForm onLeaveCreated={handleLeaveCreated} />
      <LeaveList refreshKey={refreshKey} />
    </div>
  );
};

export default LeavesPage;
