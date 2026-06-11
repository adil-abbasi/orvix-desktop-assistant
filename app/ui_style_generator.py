def generate_professional_css(theme=None):
    theme_name = "modern"

    primary = "#020617"
    secondary = "#d4af37"
    accent = "#8b5cf6"
    surface = "#0f172a"
    surface_light = "#1e293b"
    text = "#f8fafc"
    muted = "#cbd5e1"
    border = "rgba(255, 255, 255, 0.12)"

    if isinstance(theme, str):
        theme_name = theme.lower().strip()

    if isinstance(theme, dict):
        theme_name = theme.get("theme", theme_name)
        primary = theme.get("primary", primary)
        secondary = theme.get("secondary", secondary)
        accent = theme.get("accent", accent)

    if theme_name == "premium":
        primary = "#030712"
        secondary = "#d4af37"
        accent = "#8b5cf6"
        surface = "#111827"
        surface_light = "#1f2937"
        text = "#f9fafb"
        muted = "#d1d5db"

    elif theme_name == "futuristic":
        primary = "#020617"
        secondary = "#22d3ee"
        accent = "#a855f7"
        surface = "#0f172a"
        surface_light = "#1e1b4b"
        text = "#f8fafc"
        muted = "#bae6fd"

    elif theme_name == "minimal":
        primary = "#f8fafc"
        secondary = "#111827"
        accent = "#2563eb"
        surface = "#ffffff"
        surface_light = "#e5e7eb"
        text = "#111827"
        muted = "#4b5563"
        border = "rgba(17, 24, 39, 0.14)"

    elif theme_name == "medical":
        primary = "#ecfdf5"
        secondary = "#059669"
        accent = "#0ea5e9"
        surface = "#ffffff"
        surface_light = "#d1fae5"
        text = "#064e3b"
        muted = "#374151"
        border = "rgba(6, 78, 59, 0.14)"

    elif theme_name == "business":
        primary = "#111827"
        secondary = "#2563eb"
        accent = "#10b981"
        surface = "#1f2937"
        surface_light = "#374151"
        text = "#f9fafb"
        muted = "#d1d5db"

    elif theme_name == "portfolio":
        primary = "#020617"
        secondary = "#8b5cf6"
        accent = "#06b6d4"
        surface = "#111827"
        surface_light = "#1e293b"
        text = "#f8fafc"
        muted = "#cbd5e1"

    elif theme_name == "technology":
        primary = "#020617"
        secondary = "#22d3ee"
        accent = "#a855f7"
        surface = "#0f172a"
        surface_light = "#1e293b"
        text = "#f8fafc"
        muted = "#bae6fd"

    return f"""
* {{
  box-sizing: border-box;
}}

html {{
  scroll-behavior: smooth;
}}

body {{
  margin: 0;
  font-family: Inter, Segoe UI, Arial, sans-serif;
  background:
    radial-gradient(circle at top left, {secondary}33, transparent 30%),
    radial-gradient(circle at bottom right, {accent}22, transparent 28%),
    {primary};
  color: {text};
}}

a {{
  color: inherit;
  text-decoration: none;
}}

button {{
  font-family: inherit;
  cursor: pointer;
}}

.app-layout {{
  min-height: 100vh;
}}

.navbar {{
  position: sticky;
  top: 0;
  z-index: 50;
  min-height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  padding: 18px 46px;
  background: rgba(15, 23, 42, 0.84);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid {border};
}}

.brand {{
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: {text};
  white-space: nowrap;
}}

.nav-links {{
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}}

.nav-link {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 15px;
  border-radius: 999px;
  color: {muted};
  font-size: 0.95rem;
  font-weight: 600;
  transition: 0.25s ease;
}}

.nav-link:hover {{
  color: {text};
  background: rgba(255, 255, 255, 0.10);
  transform: translateY(-1px);
}}

.page {{
  min-height: calc(100vh - 76px);
  padding: 46px 24px 80px;
}}

.hero-section {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 78px 34px 58px;
  border-radius: 34px;
}}

.premium-hero {{
  background:
    linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03)),
    radial-gradient(circle at top right, {secondary}44, transparent 35%),
    {surface};
  border: 1px solid {border};
  box-shadow: 0 30px 100px rgba(0, 0, 0, 0.35);
}}

.eyebrow {{
  display: inline-flex;
  align-items: center;
  margin: 0 0 18px;
  color: {secondary};
  font-size: 0.82rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}}

.hero-section h1 {{
  max-width: 980px;
  margin: 0;
  font-size: clamp(2.4rem, 6vw, 5.6rem);
  line-height: 0.96;
  letter-spacing: -0.075em;
}}

.hero-section p {{
  max-width: 820px;
  margin: 24px 0 0;
  color: {muted};
  font-size: 1.12rem;
  line-height: 1.8;
}}

.hero-actions {{
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 34px;
}}

.primary-btn,
.secondary-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 12px 20px;
  border-radius: 999px;
  font-weight: 800;
  transition: 0.25s ease;
}}

.primary-btn {{
  background: linear-gradient(135deg, {secondary}, {accent});
  color: #ffffff;
  box-shadow: 0 18px 45px {secondary}33;
}}

.secondary-btn {{
  color: {text};
  border: 1px solid {border};
  background: rgba(255, 255, 255, 0.07);
}}

.primary-btn:hover,
.secondary-btn:hover {{
  transform: translateY(-3px);
}}

.content-grid {{
  max-width: 1180px;
  margin: 28px auto 0;
  padding: 0 4px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 22px;
}}

.card {{
  position: relative;
  min-height: 230px;
  padding: 30px;
  border-radius: 28px;
  background:
    linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04)),
    {surface};
  border: 1px solid {border};
  box-shadow: 0 28px 80px rgba(0, 0, 0, 0.28);
  overflow: hidden;
  transition: 0.25s ease;
}}

.card::before {{
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, {secondary}22, transparent 32%);
  opacity: 0;
  transition: 0.25s ease;
}}

.card:hover {{
  transform: translateY(-7px);
  border-color: {secondary};
}}

.card:hover::before {{
  opacity: 1;
}}

.card-number {{
  position: relative;
  display: inline-flex;
  margin-bottom: 34px;
  color: {secondary};
  font-size: 0.95rem;
  font-weight: 900;
  letter-spacing: 0.12em;
}}

.card h2 {{
  position: relative;
  margin: 0 0 14px;
  font-size: 1.45rem;
  letter-spacing: -0.03em;
}}

.card p {{
  position: relative;
  margin: 0;
  color: {muted};
  line-height: 1.75;
}}

.text-link {{
  position: relative;
  display: inline-flex;
  margin-top: 20px;
  color: {secondary};
  font-weight: 800;
}}

.highlight-section {{
  max-width: 1120px;
  margin: 34px auto 0;
  padding: 46px;
  border-radius: 34px;
  background:
    linear-gradient(135deg, {secondary}33, {accent}22),
    {surface_light};
  border: 1px solid {border};
}}

.highlight-section h2 {{
  margin: 0 0 14px;
  font-size: clamp(1.8rem, 4vw, 3.2rem);
  letter-spacing: -0.05em;
}}

.highlight-section p {{
  max-width: 820px;
  margin: 0;
  color: {muted};
  line-height: 1.8;
}}

.skill-cloud {{
  max-width: 1120px;
  margin: 0 auto 32px;
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  padding: 0 4px;
}}

.skill-pill {{
  display: inline-flex;
  align-items: center;
  padding: 13px 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid {border};
  color: {text};
  font-weight: 800;
}}

.contact-panel {{
  display: grid;
  gap: 12px;
}}

.stat-card h2 {{
  font-size: 3rem;
  color: {secondary};
}}

.hero {{
  padding: 60px;
  border-radius: 28px;
  background: linear-gradient(135deg, {surface}, {primary});
}}

.card-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 30px;
}}

.badge {{
  display: inline-block;
  padding: 7px 14px;
  border-radius: 999px;
  background: {secondary};
  color: white;
  font-weight: 800;
}}

@media (max-width: 780px) {{
  .navbar {{
    align-items: flex-start;
    flex-direction: column;
    padding: 18px 22px;
  }}

  .nav-links {{
    justify-content: flex-start;
  }}

  .page {{
    padding: 26px 14px 56px;
  }}

  .hero-section {{
    padding: 52px 22px 38px;
  }}

  .content-grid {{
    grid-template-columns: 1fr;
  }}

  .highlight-section {{
    padding: 30px;
  }}
}}
"""