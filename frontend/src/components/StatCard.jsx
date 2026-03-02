import './StatCard.css';

const StatCard = ({ icon, label, value, gradient, suffix = '' }) => {
  return (
    <div className="stat-card" style={gradient ? { background: gradient } : {}}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <h3>{label}</h3>
        <p className="stat-value">
          {value}
          {suffix && <span className="stat-suffix">{suffix}</span>}
        </p>
      </div>
    </div>
  );
};

export default StatCard;
