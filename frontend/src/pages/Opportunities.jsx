import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken, getAllOpportunities, getStudentMatches, getStudentProfile } from '../api';
import OpportunityCard from '../components/OpportunityCard';
import '../styles/main.css';

const Opportunities = () => {
  const [opportunities, setOpportunities] = useState([]);
  const [matches, setMatches] = useState([]);
  const [student, setStudent] = useState(null);
  const [filter, setFilter] = useState(null); // null = all, true = internal, false = external
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      navigate('/login');
      return;
    }

    loadOpportunities();
  }, [filter, navigate]);

  const loadOpportunities = async () => {
    try {
      setLoading(true);
      const studentId = 1; // In real app, get from context/token
      
      const [oppsData, matchesData, profileData] = await Promise.all([
        getAllOpportunities(filter),
        getStudentMatches(studentId),
        getStudentProfile(studentId)
      ]);

      setOpportunities(oppsData);
      setMatches(matchesData);
      setStudent(profileData);
    } catch (err) {
      setError(err.message || 'Failed to load opportunities');
    } finally {
      setLoading(false);
    }
  };

  const getMatchForOpportunity = (oppId) => {
    return matches.find(m => m.opportunity_id === oppId);
  };

  const handleApplySuccess = () => {
    loadOpportunities();
  };

  if (loading) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading opportunities...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="card">
          <p className="error">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ marginBottom: '16px' }}>All Opportunities</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
          Browse internships and projects. Your fit scores are calculated automatically.
        </p>

        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setFilter(null)}
            className={`btn ${filter === null ? 'btn-primary' : 'btn-outline'}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter(true)}
            className={`btn ${filter === true ? 'btn-primary' : 'btn-outline'}`}
          >
            Internal
          </button>
          <button
            onClick={() => setFilter(false)}
            className={`btn ${filter === false ? 'btn-primary' : 'btn-outline'}`}
          >
            External
          </button>
        </div>
      </div>

      {opportunities.length === 0 ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No opportunities found. Check back later!
          </p>
        </div>
      ) : (
        <div>
          {opportunities.map((opp) => {
            const match = getMatchForOpportunity(opp.id);
            return (
              <OpportunityCard
                key={opp.id}
                opportunity={{
                  id: opp.id,
                  title: opp.title,
                  type: opp.type,
                  is_internal: opp.is_internal,
                  creator_name: opp.creator_name,
                  required_skills: opp.required_skills || [],
                  min_cgpa: opp.min_cgpa
                }}
                fitScore={match?.fit_score}
                eligible={match?.eligible}
                missingSkills={match?.missing_skills}
                reason={match?.reason}
                studentId={student?.id}
                onApplySuccess={handleApplySuccess}
              />
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Opportunities;

