import { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from './APIconfig';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/login`, { username, password });
      const token = response.data.token;
      const userId = response.data.user_id;
      if (token) {
        // Base64 encode the token and user_id for basic security
        localStorage.setItem('appToken', btoa(token));
        localStorage.setItem('userId', btoa(userId));
        window.location.reload();
      } else {
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow-sm p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 className="text-center mb-4">Login</h2>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input
            type="text"
            id="username"
            className="form-control"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            id="password"
            className="form-control"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button onClick={handleLogin} className="btn btn-primary w-100">Login</button>
      </div>
    </div>
  );
}

export default Login;
