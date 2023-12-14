import smtplib
from email.mime.text import MIMEText
from dotenv import dotenv_values


def send_email(
    recipient: str,
    subject: str,
    body: str
):
    email_cred = dotenv_values(".env")

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.ehlo()
        server.starttls()
        server.login(
            user=email_cred["EMAIL"],
            password=email_cred["APP_PASS"]
        )

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = email_cred["EMAIL"]
        message["To"] = recipient

        server.sendmail(email_cred["APP_PASS"], recipient, message.as_string())

        server.close()
