import os
import smtplib
from email.message import EmailMessage

# Read credentials from environment variables (passed by GitHub Actions)
EMAIL_ADDRESS = os.environ.get("MAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
RECEIVER_EMAIL = os.environ.get("MAIL_RECEIVER", EMAIL_ADDRESS)

# Open the report file (fixing the FileNotFoundError from earlier)
with open("report.json", "r") as f:
  report_data = f.read()

# Build the email
msg = EmailMessage()
msg.Subject = "Automated Assignment Report"
msg.From = EMAIL_ADDRESS
msg.To = RECEIVER_EMAIL
msg.set_content(
    f"Here is your automated report generated from GitHub Actions:\n\n{report_data}"
)

# Send the email via SMTP (using Gmail as an example)
try:
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
  print("Email sent successfully!")
except Exception as e:
  print(f"Failed to send email: {e}")