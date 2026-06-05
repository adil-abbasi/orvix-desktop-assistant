import json
import re


from app.ai.providers import ask_ai


def extract_json(text):
    if not text:
        return None

    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)

    if match:
        try:
            return json.loads(match.group(0))
        except Exception as e:
            print("DEBUG CHANGE JSON ERROR:", e)
            return None

    return None


def fallback_login_changes(project_files):
    app_path = None

    for path in project_files.keys():
        if path.endswith("src\\App.jsx") or path.endswith("src/App.jsx"):
            app_path = path
            break

    app_code = project_files.get(app_path, "") if app_path else ""

    login_code = '''import React, { useState } from "react";

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
'''

    if app_code and 'import Login from "./pages/Login";' not in app_code:
        app_code = app_code.replace(
            'import "./style.css";',
            'import Login from "./pages/Login";\nimport "./style.css";'
        )

    if app_code and '<Route path="/login"' not in app_code:
        app_code = app_code.replace(
            "</Routes>",
            '          <Route path="/login" element={<Login />} />\n        </Routes>'
        )

    if app_code and '<Link to="/login">' not in app_code:
        app_code = app_code.replace(
            "</nav>",
            '          <Link to="/login">Login</Link>\n      </nav>'
        )

    return {
        "src/pages/Login.jsx": login_code,
        "src/App.jsx": app_code
    }


def generate_file_changes(request, project_files, modification_plan):
    lower_request = request.lower()

    if "login" in lower_request:
        print("DEBUG USING SAFE LOGIN FALLBACK")
        return fallback_login_changes(project_files)

    compact_files = {}

    for path, content in project_files.items():
        compact_files[path] = content[:3000]

    prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

You are Orvix AI code editor.

User request:
{request}

Modification plan:
{modification_plan}

Existing project files:
{compact_files}

Return JSON:
{{
  "src/pages/Login.jsx": "full file code",
  "src/App.jsx": "full updated file code"
}}

Strict rules:
- JSON must be parseable by Python json.loads.
- Escape all newlines as \\n.
- Escape all double quotes inside code.
- Do not add Signup unless user asks for Signup.
- Do not import files that are not created.
- Use valid React JSX only.
"""

    result = ask_ai(prompt)

    print("=" * 60)
    print("DEBUG CHANGE RESULT:")
    print(result)
    print("=" * 60)

    if result.get("success"):
        parsed = extract_json(result.get("response", ""))

        print("DEBUG PARSED:")
        print(parsed)

        if isinstance(parsed, dict):
            return parsed

    if "login" in lower_request:
        print("DEBUG USING FALLBACK LOGIN CHANGES")
        return fallback_login_changes(project_files)

    return {}