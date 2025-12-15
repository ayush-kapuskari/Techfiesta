import { Link, useNavigate } from 'react-router-dom';
import { removeToken } from '../api';
import '../styles/main.css';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  return (
    <nav style={{
      background: 'white',
      borderBottom: '1px solid var(--border)',
      padding: '16px 0',
      marginBottom: '32px'
    }}>
      <div className="container" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <Link to="/" style={{
          textDecoration: 'none',
          color: 'var(--primary)',
          fontSize: '1.5rem',
          fontWeight: 700
        }}>
          OpportuneX
        </Link>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          {token ? (
            <>
              <Link to="/dashboard" style={{
                textDecoration: 'none',
                color: 'var(--text-primary)',
                fontWeight: 500
              }}>
                Dashboard
              </Link>
              <Link to="/opportunities" style={{
                textDecoration: 'none',
                color: 'var(--text-primary)',
                fontWeight: 500
              }}>
                Opportunities
              </Link>
              <button
                onClick={handleLogout}
                className="btn btn-outline"
                style={{ padding: '8px 16px' }}
              >
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" style={{
              textDecoration: 'none',
              color: 'var(--primary)',
              fontWeight: 500
            }}>
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

