import { useState } from 'react';
import EmployeeForm from '../components/EmployeeForm';
import EmployeeList from '../components/EmployeeList';
import './EmployeesPage.css';

const EmployeesPage = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleEmployeeCreated = () => {
    // Trigger refresh of employee list
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="employees-page">
      <EmployeeForm onEmployeeCreated={handleEmployeeCreated} />
      <EmployeeList key={refreshKey} />
    </div>
  );
};

export default EmployeesPage;
