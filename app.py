import json, os
from urllib.parse import urlparse
from flask import Flask, request, render_template_string

app = Flask(__name__)
DATA_FILE = os.environ.get("DATA_FILE", "submissions.json")

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)

def valid_url(u):
    p = urlparse(u)
    return p.scheme in ("http", "https") and bool(p.netloc)

def validate(form):
    errors = []
    for field, label in [("name", "Name"), ("reg_no", "Registration number"),
                         ("title", "Assignment title"), ("url", "Submission URL")]:
        if not form.get(field, "").strip():
            errors.append(f"{label} is required")
    # DEFECT (email demo): URL validation is disabled on purpose
    if False:
        errors.append("Submission URL is invalid")
    return errors

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assignment Submission Portal</title>
<style>
  * { box-sizing: border-box; }

  /* ===== Education themed background ===== */
  body {
    margin: 0;
    min-height: 100vh;
    font-family: "Segoe UI", system-ui, -apple-system, Roboto, sans-serif;
    color: #1f2937;
    padding: 40px 16px;
    background:
      url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240' viewBox='0 0 240 240' fill='none' stroke='white' stroke-opacity='0.16' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M10 30 L40 16 L70 30 L40 44 Z'/><path d='M22 36 V50 C30 58 50 58 58 50 V36'/><path d='M70 30 V46'/><path d='M130 24 C142 19 152 21 160 27 C168 21 178 19 190 24 V52 C178 47 168 49 160 55 C152 49 142 47 130 52 Z'/><path d='M160 27 V55'/><path d='M25 190 L30 170 L65 135 L80 150 L45 185 Z'/><path d='M58 142 L73 157'/><path d='M165 140 C150 140 143 155 150 168 C154 174 156 177 156 182 H174 C174 177 176 174 180 168 C187 155 180 140 165 140 Z'/><path d='M158 190 H172'/><path d='M161 197 H169'/><circle cx='110' cy='110' r='3'/><circle cx='215' cy='95' r='3'/><circle cx='100' cy='205' r='3'/></svg>"),
      radial-gradient(circle at 15% 10%, rgba(251, 191, 36, 0.28), transparent 40%),
      radial-gradient(circle at 85% 90%, rgba(236, 72, 153, 0.25), transparent 45%),
      linear-gradient(135deg, #1e1b4b, #312e81 55%, #4338ca);
    background-attachment: fixed;
  }

  .container { max-width: 760px; margin: 0 auto; position: relative; z-index: 1; }

  header { text-align: center; color: #fff; margin-bottom: 28px; }
  header h1 {
    margin: 0 0 6px;
    font-size: 2.2rem;
    letter-spacing: -0.5px;
    text-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);
  }
  header p { margin: 0; opacity: 0.85; }

  .logo {
    width: 78px;
    height: 78px;
    margin: 0 auto 14px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.4rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  }

  .card {
    position: relative;
    overflow: hidden;
    background: #fff;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
  }
  .card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 6px;
    background: linear-gradient(90deg, #fbbf24, #f472b6, #6366f1, #34d399);
  }
  .card h2 { margin: 0 0 18px; font-size: 1.25rem; }

  .field { margin-bottom: 16px; }
  label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 6px; color: #4b5563; }
  input {
    width: 100%;
    padding: 12px 14px;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    font-size: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  input:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.18);
  }
  button {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
  }
  button:hover { transform: translateY(-2px); box-shadow: 0 8px 18px rgba(79, 70, 229, 0.4); }

  .alert { padding: 12px 16px; border-radius: 10px; margin-bottom: 12px; font-size: 0.95rem; }
  .alert.error { background: #fef2f2; color: #b91c1c; border-left: 5px solid #ef4444; }
  .alert.success { background: #ecfdf5; color: #047857; border-left: 5px solid #10b981; }

  .badge {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    margin-left: 8px;
  }
  ul { list-style: none; margin: 0; padding: 0; }
  .item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    border: 1px solid #eef0f4;
    border-radius: 12px;
    margin-bottom: 10px;
    transition: background 0.2s, transform 0.2s;
  }
  .item:hover { background: #f9fafb; transform: translateX(4px); }
  .avatar {
    flex: 0 0 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    color: #fff;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .info { min-width: 0; }
  .info strong { display: block; }
  .info small { color: #6b7280; }
  .info a { color: #4f46e5; text-decoration: none; word-break: break-all; }
  .info a:hover { text-decoration: underline; }
  .empty { text-align: center; color: #9ca3af; padding: 20px 0; }
  footer { text-align: center; color: rgba(255, 255, 255, 0.75); font-size: 0.85rem; }

  /* ===== Floating school icons ===== */
  .floaty {
    position: fixed;
    font-size: 2.2rem;
    opacity: 0.35;
    pointer-events: none;
    animation: float 7s ease-in-out infinite;
    z-index: 0;
  }
  .f1 { top: 8%;  left: 6%;  animation-delay: 0s; }
  .f2 { top: 20%; right: 7%; animation-delay: 1.2s; }
  .f3 { top: 60%; left: 4%;  animation-delay: 2.4s; }
  .f4 { top: 75%; right: 6%; animation-delay: 3.6s; }
  .f5 { top: 40%; right: 3%; animation-delay: 4.8s; }
  @keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50%      { transform: translateY(-18px) rotate(6deg); }
  }
</style>
</head>
<body>
  <div class="floaty f1">📚</div>
  <div class="floaty f2">✏️</div>
  <div class="floaty f3">🎓</div>
  <div class="floaty f4">💡</div>
  <div class="floaty f5">🔬</div>

  <div class="container">
    <header>
      <div class="logo">🎓</div>
      <h1>Assignment Submission Portal</h1>
      <p>Learn. Build. Submit.</p>
    </header>

    <div class="card">
      <h2>New submission</h2>

      {% for e in errors %}<div class="alert error">{{ e }}</div>{% endfor %}
      {% if ok %}<div class="alert success">Submission saved!</div>{% endif %}

      <form method="post">
        <div class="field">
          <label>Full name</label>
          <input name="name" placeholder="e.g. Ali Khan">
        </div>
        <div class="field">
          <label>Registration number</label>
          <input name="reg_no" placeholder="e.g. FA23-BS-025">
        </div>
        <div class="field">
          <label>Assignment title</label>
          <input name="title" placeholder="e.g. DevOps Lab 1">
        </div>
        <div class="field">
          <label>Submission URL</label>
          <input name="url" placeholder="https://github.com/you/project">
        </div>
        <button type="submit">Submit assignment</button>
      </form>
    </div>

    <div class="card">
      <h2>Saved submissions <span class="badge">{{ items|length }}</span></h2>
      {% if items %}
      <ul>
        {% for s in items %}
        <li class="item">
          <div class="avatar">{{ s.name[0]|upper }}</div>
          <div class="info">
            <strong>{{ s.title }}</strong>
            <small>{{ s.name }} &middot; {{ s.reg_no }}</small><br>
            <a href="{{ s.url }}" target="_blank">{{ s.url }}</a>
          </div>
        </li>
        {% endfor %}
      </ul>
      {% else %}
      <p class="empty">No submissions yet.</p>
      {% endif %}
    </div>

    <footer>CSC418 DevOps &middot; Lab Midterm</footer>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    errors, ok = [], False
    if request.method == "POST":
        errors = validate(request.form)
        if not errors:
            items = load()
            items.append({k: request.form[k].strip() for k in ("name", "reg_no", "title", "url")})
            save(items)
            ok = True
    return render_template_string(PAGE, errors=errors, ok=ok, items=load())

if __name__ == "__main__":
    app.run(debug=True)