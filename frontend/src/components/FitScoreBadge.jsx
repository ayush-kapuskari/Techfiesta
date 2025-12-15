import '../styles/main.css';

const FitScoreBadge = ({ score, eligible }) => {
  const getBadgeClass = () => {
    if (score >= 80) return 'badge-success';
    if (score >= 50) return 'badge-warning';
    return 'badge-danger';
  };

  return (
    <span className={`badge ${getBadgeClass()}`}>
      Fit Score: {score}%
    </span>
  );
};

export default FitScoreBadge;

