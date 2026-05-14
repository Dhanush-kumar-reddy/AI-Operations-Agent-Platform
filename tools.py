import os
import smtplib

from email.mime.text import MIMEText

from dotenv import load_dotenv

from database import (
    SessionLocal,
    Meeting,
    Contact
)

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")

EMAIL_PASS = os.getenv("EMAIL_PASS")


# =========================
# SEND EMAIL
# =========================

def send_email(person, content):

    db = SessionLocal()

    try:

        if not person:

            return "Email failed: No recipient provided"

        normalized_person = person.strip().lower()

        contact = db.query(Contact).filter(
            Contact.name.ilike(normalized_person)
        ).first()

        if not contact:

            return (
                f"Email failed: "
                f"No email found for {person}"
            )

        to_email = contact.email

        if not to_email:

            return (
                f"Email failed: "
                f"No email found for {person}"
            )

        msg = MIMEText(content)

        msg["Subject"] = "Automated Message"

        msg["From"] = EMAIL_USER

        msg["To"] = to_email

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_USER,
                EMAIL_PASS
            )

            server.send_message(msg)

        return f"Email sent to {to_email}"

    except Exception as e:

        return f"Email failed: {str(e)}"

    finally:

        db.close()


# =========================
# SCHEDULE MEETING
# =========================

def schedule_meeting(person, time):

    db = SessionLocal()

    try:

        if not person:

            return (
                "Meeting failed: "
                "No person provided"
            )

        meeting = Meeting(
            person=person.strip(),
            time=time
        )

        db.add(meeting)

        db.commit()

        return (
            f"Meeting scheduled with "
            f"{person} at {time}"
        )

    except Exception as e:

        return f"Meeting failed: {str(e)}"

    finally:

        db.close()