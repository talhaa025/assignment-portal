import json, os, smtplib
from email.message import EmailMessage

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
msg["From"] = os.environ["MAIL_USER"]
msg["To"] = os.environ["MAIL_TO"]
msg.set_content("\n".join(lines))
msg.add_attachment(json.dumps(r, indent=2).encode(),
                   maintype="application", subtype="json",
                   filename="test-report.json")

with smtplib.SMTP_SSL(os.environ["MAIL_SERVER"], 465) as server:
    server.login(os.environ["MAIL_USER"], os.environ["MAIL_PASS"])
    server.send_message(msg)
print("Email sent to", os.environ["MAIL_TO"])