import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from config.config        import GMAIL_ADDRESS, GMAIL_APP_PASSWORD


def send_email(subject: str, html_body: str, recipients: list[str]) -> bool:
    """
    Send an HTML email via Gmail SMTP.

    Setup steps:
    1. Go to Google Account → Security → 2-Step Verification → App Passwords
    2. Create an App Password for "Mail"
    3. Put that 16-char password in .env as GMAIL_APP_PASSWORD
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("[EmailTool] Gmail credentials not set in .env")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = ", ".join(recipients)

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, recipients, msg.as_string())
        print(f"[EmailTool] Sent to {recipients}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EmailTool] Authentication failed. Check GMAIL_APP_PASSWORD in .env")
        return False
    except Exception as e:
        print(f"[EmailTool] Error: {e}")
        return False