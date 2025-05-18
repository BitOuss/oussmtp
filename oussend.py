import smtplib
import time
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging

# ANSI escape sequences for coloring output
GREEN   = "\033[32m"
RED     = "\033[31m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
MAGENTA = "\033[35m"
RESET   = "\033[0m"

# Custom logging formatter using ANSI colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        if record.levelno == logging.INFO:
            msg = GREEN + msg + RESET
        elif record.levelno == logging.ERROR:
            msg = RED + msg + RESET
        elif record.levelno == logging.WARNING:
            msg = YELLOW + msg + RESET
        return msg

# Setup logger with our custom formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(ColoredFormatter())
logger.handlers = []  # Clear default handlers
logger.addHandler(ch)

def print_banner():
    banner = f"""
{CYAN}******************************************
*        Oussend (v1.0)                   * 
*         SMTP Email Sender               *
******************************************{RESET}
"""
    print(banner)

# SMTP Configuration
SMTP_HOST = 'smtp.yourserver.com'
SMTP_PORT = 587
SMTP_USER = 'your@email.com'
SMTP_PASS = 'yourpassword'

# Email Info
SENDER_NAME = 'sender'
RECIPIENT = 'target@example.com'
SUBJECT = 'Test Email from Oussend'
HTML_BODY = """
<html>
  <body>
    <h1>Hello from Oussend!</h1>
    <p>This is a test email sent using <b>Python & smtplib</b>.</p>
  </body>
</html>
"""

def send_email():
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((SENDER_NAME, SMTP_USER))
        msg['To'] = RECIPIENT
        msg['Subject'] = SUBJECT
        msg['Message-ID'] = str(uuid.uuid4())

        msg.attach(MIMEText(HTML_BODY, 'html'))

        logger.info(f"Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        logger.info(f"Sending email to {RECIPIENT}...")
        server.sendmail(SMTP_USER, RECIPIENT, msg.as_string())
        server.quit()

        logger.info("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        logger.error("Authentication failed. Check your SMTP credentials.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print_banner()
    send_email()