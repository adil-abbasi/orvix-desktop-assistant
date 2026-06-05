import { useState } from 'react';
import Login from './pages/Login';

const App = () => {
  return (
    <div>
      <h1>Welcome to the App</h1>
      <nav>
        <a href="/">Home</a>
        <a href="/login">Login</a>
      </nav>
      <main>
        <Login />
      </main>
    </div>
  );
};

export default App;