FEATURE = {
    "name": "login",

    "keywords": [
        "login",
        "signin",
        "sign in",
        "auth",
        "authentication"
    ],

    "dependencies": [],

    "files": {
        "src/pages/Login.jsx": '''
function Login() {
  return (
    <section className="page">
      <h1>Login</h1>

      <input placeholder="Email" />

      <input
        type="password"
        placeholder="Password"
      />

      <button>Login</button>
    </section>
  );
}

export default Login;
'''
    }
}