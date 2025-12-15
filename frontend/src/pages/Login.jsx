import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register, setToken } from '../api';
import '../styles/main.css';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    branch: '',
    year: '',
    cgpa: '',
    role: 'student'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let response;
      if (isLogin) {
        response = await login(formData.email, formData.password);
      } else {
        const registerData = {
          email: formData.email,
          password: formData.password,
          role: formData.role,
        };
        
        if (formData.role === 'student') {
          registerData.name = formData.name;
          registerData.branch = formData.branch;
          registerData.year = parseInt(formData.year);
          registerData.cgpa = parseFloat(formData.cgpa);
        } else if (formData.role === 'faculty') {
          registerData.name = formData.name;
          registerData.department = formData.branch; // Using branch field for department
        } else if (formData.role === 'company') {
          registerData.name = formData.name;
        }

        response = await register(registerData);
      }

      if (response.access_token) {
        setToken(response.access_token);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>
          {isLogin ? 'Login to OpportuneX' : 'Create Account'}
        </h2>

        <div style={{ marginBottom: '20px', display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setIsLogin(true)}
            className={`btn ${isLogin ? 'btn-primary' : 'btn-outline'}`}
            style={{ flex: 1 }}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`btn ${!isLogin ? 'btn-primary' : 'btn-outline'}`}
            style={{ flex: 1 }}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div>
            <label className="label">Email</label>
            <input
              type="email"
              name="email"
              className="input"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="label">Password</label>
            <input
              type="password"
              name="password"
              className="input"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {!isLogin && (
            <>
              <div>
                <label className="label">Role</label>
                <select
                  name="role"
                  className="input"
                  value={formData.role}
                  onChange={handleChange}
                  required
                >
                  <option value="student">Student</option>
                  <option value="faculty">Faculty</option>
                  <option value="company">Company</option>
                </select>
              </div>

              <div>
                <label className="label">Name</label>
                <input
                  type="text"
                  name="name"
                  className="input"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>

              {formData.role === 'student' && (
                <>
                  <div>
                    <label className="label">Branch</label>
                    <input
                      type="text"
                      name="branch"
                      className="input"
                      value={formData.branch}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Year</label>
                    <input
                      type="number"
                      name="year"
                      className="input"
                      value={formData.year}
                      onChange={handleChange}
                      min="1"
                      max="6"
                      required
                    />
                  </div>
                  <div>
                    <label className="label">CGPA</label>
                    <input
                      type="number"
                      name="cgpa"
                      className="input"
                      value={formData.cgpa}
                      onChange={handleChange}
                      min="0"
                      max="10"
                      step="0.1"
                      required
                    />
                  </div>
                </>
              )}

              {formData.role === 'faculty' && (
                <div>
                  <label className="label">Department</label>
                  <input
                    type="text"
                    name="branch"
                    className="input"
                    value={formData.branch}
                    onChange={handleChange}
                    required
                  />
                </div>
              )}
            </>
          )}

          {error && <p className="error">{error}</p>}

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '16px' }}
            disabled={loading}
          >
            {loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;

