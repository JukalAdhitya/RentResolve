import logging
from app.db.models import EmailLog, Issue
from datetime import datetime

logger = logging.getLogger(__name__)

async def send_email(to: str, subject: str, body: str, issue_id: str):
    # Create EmailLog entry (Optimistic logging)
    issue = await Issue.get(issue_id)
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from app.core.config import settings

        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials missing. Falling back to MOCK email.")
            logger.info(f"--- MOCK EMAIL ---")
            logger.info(f"To: {to}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body: {body[:50]}...")
            status = "mock_sent"
        else:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.SMTP_USER, to, text)
            server.quit()
            logger.info(f"Email sent successfully to {to}")
            status = "sent"

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        status = f"failed: {str(e)}"
        
    if issue:
        email_log = EmailLog(
            recipient=to,
            subject=subject,
            status=status,
            timestamp=datetime.now()
        )
        issue.emails.append(email_log)
        await issue.save()
        
    return status == "sent" or status == "mock_sent"
