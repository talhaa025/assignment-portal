import os
import smtplib
from email.message import EmailMessage

# Read exact secret names from environment variables
EMAIL_ADDRESS = os.environ.get("MAIL_USER")
EMAIL_PASSWORD = os.environ.get("MAIL_PASS")

# Fallback chain for the recipient email
RECEIVER_EMAIL = (
    os.environ.get("MAIL_RECEIVER")
    or os.environ.get("MAIL_TO")
    or EMAIL_ADDRESS
)

# Open your report file (adjust name if it's test-report.json)
try:
  with open("report.json", "r") as f:
    report_data = f.read()
except FileNotFoundError:
  with open("test-report.json", "r") as f:
    report_data = f.read()

# Build the email
msg = EmailMessage()
msg.Subject = "Automated Assignment Report"
msg.From = EMAIL_ADDRESS
msg.To = RECEIVER_EMAIL
msg.set_content(
    f"Here is your automated report generated from GitHub Actions:\n\n{report_data}"
)

# Send the email via Gmail SMTP
try:
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
  print("Email sent successfully!")
except Exception as e:
  print(f"Failed to send email: {e}")