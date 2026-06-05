import React, { useState } from "react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    alert("Login submitted");
  }

  return (
    <section className="page">
      <div className="hero">
        <span className="badge">Login</span>
        <h1>Welcome Back</h1>
        <p>Login to continue to your account.</p>

        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: "420px" }}>
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />

          <label style={{ display: "flex", gap: "8px", alignItems: "center" }}>
            <input type="checkbox" />
            Remember me
          </label>

          <a href="#" className="link">Forgot password?</a>

          <button type="submit">Login</button>
        </form>
      </div>
    </section>
  );
}

export default Login;
