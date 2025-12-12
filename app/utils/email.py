import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "noreply@example.com"
SMTP_PASS = "password"

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
