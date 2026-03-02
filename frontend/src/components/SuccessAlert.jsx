import './SuccessAlert.css';

const SuccessAlert = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="success-alert">
      <div className="success-content">
        <span className="success-icon">✓</span>
        <span className="success-message">{message}</span>
        {onClose && (
          <button className="success-close" onClick={onClose}>
            ×
          </button>
        )}
      </div>
    </div>
  );
};

export default SuccessAlert;
