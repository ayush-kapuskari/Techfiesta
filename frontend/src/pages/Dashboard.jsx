import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken, getStudentMatches, getStudentProfile, getAllOpportunities } from '../api';
import OpportunityCard from '../components/OpportunityCard';
import '../styles/main.css';

const Dashboard = () => {
  const [student, setStudent] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      navigate('/login');
      return;
    }

    // For demo: assuming student_id is 1, in real app get from token or user context
    const studentId = 1;
    loadDashboardData(studentId);
  }, [navigate]);

  const [opportunities, setOpportunities] = useState([]);

  const loadDashboardData = async (studentId) => {
    try {
      setLoading(true);
      const [profileData, matchesData, oppsData] = await Promise.all([
        getStudentProfile(studentId),
        getStudentMatches(studentId),
        getAllOpportunities()
      ]);
      
      setStudent(profileData);
      setOpportunities(oppsData);
      // Sort matches by fit score descending
      const sortedMatches = matchesData.sort((a, b) => b.fit_score - a.fit_score);
      setMatches(sortedMatches);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleApplySuccess = () => {
    // Reload matches to update applied status
    const studentId = 1;
    getStudentMatches(studentId).then(data => {
      const sortedMatches = data.sort((a, b) => b.fit_score - a.fit_score);
      setMatches(sortedMatches);
    });
  };

  if (loading) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading...</p>
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

  const recommendedMatches = matches.filter(m => m.eligible && m.fit_score >= 50).slice(0, 6);

  return (
    <div className="container">
      <div className="card" style={{ marginBottom: '32px', background: 'linear-gradient(135deg, #2563EB 0%, #1E40AF 100%)', color: 'white' }}>
        <h1 style={{ marginBottom: '8px', color: 'white' }}>
          Welcome back{student ? `, ${student.name}` : ''}!
        </h1>
        <p style={{ color: 'rgba(255, 255, 255, 0.9)', fontSize: '16px' }}>
          Discover opportunities tailored to your skills and interests
        </p>
      </div>

      {student && (
        <div className="card" style={{ marginBottom: '32px' }}>
          <h2 style={{ marginBottom: '16px' }}>Your Profile</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
            <div>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Branch</p>
              <p style={{ fontWeight: 500 }}>{student.branch}</p>
            </div>
            <div>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Year</p>
              <p style={{ fontWeight: 500 }}>{student.year}</p>
            </div>
            <div>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>CGPA</p>
              <p style={{ fontWeight: 500 }}>{student.cgpa}</p>
            </div>
            <div>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Skills</p>
              <p style={{ fontWeight: 500 }}>{student.skills?.length || 0} skills</p>
            </div>
          </div>
        </div>
      )}

      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ marginBottom: '16px' }}>Recommended Opportunities</h2>
        {recommendedMatches.length === 0 ? (
          <div className="card">
            <p style={{ color: 'var(--text-secondary)' }}>No recommended opportunities at the moment. Check back later!</p>
          </div>
        ) : (
          <div className="grid grid-2">
            {recommendedMatches.map((match) => {
              // Find full opportunity details from matches or fetch separately
              const oppDetails = opportunities.find(o => o.id === match.opportunity_id) || {
                id: match.opportunity_id,
                title: match.opportunity,
                type: 'internship',
                is_internal: false,
                creator_name: '',
                required_skills: [],
                min_cgpa: 0
              };
              
              return (
                <OpportunityCard
                  key={match.opportunity_id}
                  opportunity={oppDetails}
                  fitScore={match.fit_score}
                  eligible={match.eligible}
                  missingSkills={match.missing_skills}
                  reason={match.reason}
                  studentId={student?.id}
                  onApplySuccess={handleApplySuccess}
                />
              );
            })}
          </div>
        )}
      </div>

      <div>
        <h2 style={{ marginBottom: '16px' }}>All Opportunities</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '16px' }}>
          View all available opportunities with your fit scores
        </p>
        <button
          onClick={() => navigate('/opportunities')}
          className="btn btn-outline"
        >
          View All Opportunities →
        </button>
      </div>
    </div>
  );
};

export default Dashboard;

