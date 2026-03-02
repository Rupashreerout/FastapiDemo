import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/">HRMS Lite</Link>
        </div>
        <ul className="navbar-menu">
          <li>
            <Link to="/" className={isActive('/')}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/employees" className={isActive('/employees')}>
              Employees
            </Link>
          </li>
          <li>
            <Link to="/attendance" className={isActive('/attendance')}>
              Attendance
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
