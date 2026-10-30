import json, os, smtplib, sys
from email.message import EmailMessage

user = os.environ.get("MAIL_USER", "").strip()
password = os.environ.get("MAIL_PASS", "").replace(" ", "").strip()
to = os.environ.get("MAIL_TO", "").strip() or user
server_name = os.environ.get("MAIL_SERVER", "").strip() or "smtp.gmail.com"

if not user or not password:
    sys.exit("MAIL_USER or MAIL_PASS is missing")

# Accept a mistaken value like https://smtp.gmail.com
server_name = server_name.replace("https://", "").replace("http://", "").strip("/")
if "gmail" not in server_name and "smtp" not in server_name:
    print("MAIL_SERVER looks wrong, using smtp.gmail.com instead of:", server_name)
    server_name = "smtp.gmail.com"

with open("final-report.json") as f:
    r = json.load(f)

s = r["summary"]
sha = str(r["commit_sha"])

lines = [
    f"Repository : {r['repository']}",
    f"Branch     : {r['branch']}",
    f"Commit     : {sha}",
    f"Run ID     : {r['run_id']}",
    f"Time (UTC) : {r['timestamp']}",
    "",
    f"OVERALL RESULT: {s['status']}",
    f"Total: {s['total']}  Passed: {s['passed']}  Failed: {s['failed']}",
    "",
    "Individual results:",
]
for t in r["tests"]:
    line = f"  [{t['result'].upper()}] {t['name']}"
    if t["failure_message"]:
        line += f"\n      {t['failure_message']}"
    lines.append(line)

msg = EmailMessage()
msg["Subject"] = f"[CI {s['status']}] {r['repository']} @ {sha[:7]}"
msg["From"] = user
msg["To"] = to
msg.set_content("\n".join(lines))
msg.add_attachment(json.dumps(r, indent=2).encode(),
                   maintype="application", subtype="json",
                   filename="test-report.json")

def send_ssl():
    with smtplib.SMTP_SSL(server_name, 465, timeout=30) as srv:
        srv.login(user, password)
        srv.send_message(msg)

def send_starttls():
    with smtplib.SMTP(server_name, 587, timeout=30) as srv:
        srv.starttls()
        srv.login(user, password)
        srv.send_message(msg)

errors = []
for name, fn in (("SSL 465", send_ssl), ("STARTTLS 587", send_starttls)):
    try:
        fn()
        print(f"Email sent to {to} via {name}")
        sys.exit(0)
    except Exception as e:
        errors.append(f"{name}: {type(e).__name__}: {e}")

print("Failed to send email:")
for e in errors:
    print("  ", e)
sys.exit(1)