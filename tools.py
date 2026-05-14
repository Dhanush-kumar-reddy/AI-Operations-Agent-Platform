import os
import smtplib
import ssl

from email.mime.text import MIMEText

from dotenv import load_dotenv

from database import (
    SessionLocal,
    Meeting,
    Contact
)


# LOAD ENV

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")

EMAIL_PASS = os.getenv("EMAIL_PASS")


# SEND EMAIL

def send_email(person, content):

    db = SessionLocal()

    try:

        print("SEND EMAIL START")

        if not EMAIL_USER or not EMAIL_PASS:

            return (
                "Email failed: "
                "EMAIL_USER or EMAIL_PASS missing"
            )

        if not person:

            return (
                "Email failed: "
                "No recipient provided"
            )

        normalized_person = (
            person.strip().lower()
        )

        print(
            "SEARCHING CONTACT:",
            normalized_person
        )

        contact = db.query(Contact).filter(
            Contact.name.ilike(
                f"%{normalized_person}%"
            )
        ).first()

        if not contact:

            return (
                f"Email failed: "
                f"No email found for {person}"
            )

        to_email = contact.email

        print(
            "EMAIL FOUND:",
            to_email
        )

        msg = MIMEText(content)

        msg["Subject"] = (
            "AI Operations Agent Notification"
        )

        msg["From"] = EMAIL_USER

        msg["To"] = to_email

        context = ssl.create_default_context()

        print("CONNECTING SMTP")

        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=20
        ) as server:

            server.ehlo()

            server.starttls(
                context=context
            )

            server.ehlo()

            print("SMTP LOGIN")

            server.login(
                EMAIL_USER,
                EMAIL_PASS
            )

            print("SENDING EMAIL")

            server.send_message(msg)

        print("EMAIL SUCCESS")

        return f"Email sent to {to_email}"

    except Exception as e:

        print(
            "SEND EMAIL ERROR:",
            str(e)
        )

        return (
            f"Email failed: "
            f"{str(e)}"
        )

    finally:

        db.close()


# SCHEDULE MEETING

def schedule_meeting(person, time):

    db = SessionLocal()

    try:

        print("SCHEDULE MEETING START")

        if not person:

            return (
                "Meeting failed: "
                "No person provided"
            )

        if not time:

            time = "Not specified"

        meeting = Meeting(
            person=person.strip(),
            time=time
        )

        db.add(meeting)

        db.commit()

        print("MEETING SUCCESS")

        return (
            f"Meeting scheduled with "
            f"{person} at {time}"
        )

    except Exception as e:

        print(
            "MEETING ERROR:",
            str(e)
        )

        return (
            f"Meeting failed: "
            f"{str(e)}"
        )

    finally:

        db.close()