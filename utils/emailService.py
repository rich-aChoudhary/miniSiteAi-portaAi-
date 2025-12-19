import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def send_welcome_email(to_email, username):
    # Create message
    message = MIMEMultipart()
    message['From'] = Config.SMTP_SENDER
    message['To'] = to_email
    message['Subject'] = 'Welcome to Our Application!'

    # Email body
    body = f"""
    Hello {username},

    Welcome to our application! We're excited to have you on board.
    Your account has been successfully created.

    Best regards,
    The Team
    """
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server
    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(message)