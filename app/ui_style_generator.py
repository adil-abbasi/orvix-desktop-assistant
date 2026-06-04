def generate_professional_css(theme=None):

    primary = "#0f172a"
    secondary = "#6366f1"
    surface = "#1e293b"
    text = "#f8fafc"

    if isinstance(theme, dict):
        primary = theme.get("primary", primary)
        secondary = theme.get("secondary", secondary)

    return f"""
* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  font-family: Inter, Segoe UI, sans-serif;
  background: {primary};
  color: {text};
}}

.navbar {{
  display:flex;
  gap:24px;
  padding:18px 32px;
  background:{surface};
}}

.navbar a {{
  color:{text};
  text-decoration:none;
}}

.hero {{
  padding:50px;
  border-radius:24px;
  background:linear-gradient(
      135deg,
      {surface},
      {primary}
  );
}}

button {{
  background:{secondary};
  border:none;
  padding:12px 18px;
  border-radius:12px;
  color:white;
}}

.card-grid {{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:24px;
  margin-top:30px;
}}

.card {{
  padding:24px;
  border-radius:18px;
  background:{surface};
}}

.badge {{
  display:inline-block;
  padding:6px 12px;
  border-radius:999px;
  background:{secondary};
}}
"""