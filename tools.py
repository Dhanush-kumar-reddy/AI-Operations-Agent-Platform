import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from database import SessionLocal, Meeting
from database import SessionLocal, Meeting, Contact

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email(person, content):
    try:
        db = SessionLocal()

        contact = db.query(Contact).filter(
            Contact.name == person.title()
        ).first()

        db.close()

        if not contact:
            return f"Email failed: No email found for {person}"

        to_email = contact.email

        if not to_email:
            return f"Email failed: No email found for {person}"

        msg = MIMEText(content)
        msg["Subject"] = "Automated Message"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return f"Email sent to {to_email}"

    except Exception as e:
        return f"Email failed: {str(e)}"


def schedule_meeting(person, time):
    try:
        db = SessionLocal()

        meeting = Meeting(person=person, time=time)
        db.add(meeting)
        db.commit()
        db.close()

        return f"Meeting scheduled with {person} at {time}"

    except Exception as e:
        return f"Meeting failed: {str(e)}"