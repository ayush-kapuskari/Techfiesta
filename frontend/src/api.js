const API_BASE_URL = 'http://127.0.0.1:8000';

// Get stored token
export const getToken = () => {
  return localStorage.getItem('token');
};

// Set token
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

// Remove token
export const removeToken = () => {
  localStorage.removeItem('token');
};

// Make API request with auth
const apiRequest = async (endpoint, options = {}) => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'An error occurred');
    }

    return data;
  } catch (error) {
    throw error;
  }
};

// Auth API
export const login = async (email, password) => {
  const data = await apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  return data;
};

export const register = async (userData) => {
  const data = await apiRequest('/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
  return data;
};

// Student API
export const getStudentMatches = async (studentId) => {
  const data = await apiRequest(`/matching/${studentId}`);
  return data;
};

export const getStudentProfile = async (studentId) => {
  const data = await apiRequest(`/student/${studentId}`);
  return data;
};

// Opportunity API
export const getAllOpportunities = async (isInternal = null) => {
  let endpoint = '/opportunity/all';
  if (isInternal !== null) {
    endpoint += `?is_internal=${isInternal}`;
  }
  const data = await apiRequest(endpoint);
  return data;
};

// Application API
export const applyToOpportunity = async (studentId, opportunityId) => {
  const data = await apiRequest('/applications/apply', {
    method: 'POST',
    body: JSON.stringify({
      student_id: studentId,
      opportunity_id: opportunityId,
    }),
  });
  return data;
};

