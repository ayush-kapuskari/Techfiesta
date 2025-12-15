import { useState } from 'react';
import FitScoreBadge from './FitScoreBadge';
import { applyToOpportunity } from '../api';
import '../styles/main.css';

const OpportunityCard = ({ opportunity, fitScore, eligible, missingSkills, reason, studentId, onApplySuccess }) => {
  const [isApplying, setIsApplying] = useState(false);
  const [error, setError] = useState(null);
  const [applied, setApplied] = useState(false);

  const handleApply = async () => {
    if (!studentId) {
      setError('Please login to apply');
      return;
    }

    setIsApplying(true);
    setError(null);

    try {
      await applyToOpportunity(studentId, opportunity.id);
      setApplied(true);
      if (onApplySuccess) {
        onApplySuccess();
      }
    } catch (err) {
      setError(err.message || 'Failed to apply');
    } finally {
      setIsApplying(false);
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div style={{ flex: 1 }}>
          <h3 style={{ marginBottom: '8px' }}>{opportunity.title}</h3>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
            <span className={`tag tag-${opportunity.type === 'internship' ? 'internship' : 'project'}`}>
              {opportunity.type.charAt(0).toUpperCase() + opportunity.type.slice(1)}
            </span>
            <span className={`tag tag-${opportunity.is_internal ? 'internal' : 'external'}`}>
              {opportunity.is_internal ? 'Internal' : 'External'}
            </span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '12px' }}>
            Created by: {opportunity.creator_name}
          </p>
          {opportunity.required_skills && opportunity.required_skills.length > 0 && (
            <div style={{ marginBottom: '12px' }}>
              <span style={{ fontSize: '14px', fontWeight: 500 }}>Skills: </span>
              <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                {opportunity.required_skills.join(', ')}
              </span>
            </div>
          )}
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
            Min CGPA: {opportunity.min_cgpa}
          </p>
        </div>
        {fitScore !== undefined && (
          <div style={{ textAlign: 'right' }}>
            <FitScoreBadge score={fitScore} eligible={eligible} />
            {!eligible && reason && (
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '8px', maxWidth: '200px' }}>
                {reason}
              </p>
            )}
          </div>
        )}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          {missingSkills && missingSkills.length > 0 && (
            <p style={{ fontSize: '12px', color: 'var(--warning)', marginTop: '8px' }}>
              Missing: {missingSkills.join(', ')}
            </p>
          )}
        </div>
        <button
          onClick={handleApply}
          disabled={isApplying || applied || !eligible}
          className={`btn ${applied ? 'btn-secondary' : 'btn-primary'}`}
          style={{
            opacity: (!eligible && !applied) ? 0.5 : 1,
            cursor: (!eligible && !applied) ? 'not-allowed' : 'pointer'
          }}
        >
          {applied ? 'Applied' : isApplying ? 'Applying...' : 'Apply'}
        </button>
      </div>
      {error && <p className="error" style={{ marginTop: '8px' }}>{error}</p>}
    </div>
  );
};

export default OpportunityCard;

