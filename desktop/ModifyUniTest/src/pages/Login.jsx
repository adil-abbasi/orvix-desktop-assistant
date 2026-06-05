import React from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [rememberMe, setRememberMe] = React.useState(false);
  const [showForgot, setShowForgot] = React.useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div>
          <label><input type="checkbox" checked={rememberMe} onChange={(e) => setRememberMe(e.target.checked)} /> Remember me</label>
        </div>
        <div>
          <button type="submit">Login</button>
        </div>
        <div>
          <Link to="/forgot">Forgot password?</Link>
        </div>
      </form>
      {showForgot && <div>Forgot password page</div>}
    </div>
  );
};

export default Login;
