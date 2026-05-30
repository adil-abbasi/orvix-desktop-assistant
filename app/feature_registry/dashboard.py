FEATURE = {
    "name": "dashboard",
    "keywords": ["dashboard", "admin panel", "admin"],
    "dependencies": [],
    "files": {
        "src/pages/Dashboard.jsx": '''function Dashboard() {
  return (
    <section className="page">
      <h1>Dashboard</h1>
      <p>Manage your application data here.</p>
    </section>
  );
}

export default Dashboard;
'''
    }
}