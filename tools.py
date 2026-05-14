import os
import ssl
import resend

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


def send_email(person, content):

    db = SessionLocal()

    try:

        print("SEND EMAIL START")

        resend.api_key = os.getenv(
            "RESEND_API_KEY"
        )

        if not resend.api_key:

            return (
                "Email failed: "
                "Missing RESEND_API_KEY"
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

        params = {
            "from": "onboarding@resend.dev",
            "to": [to_email],
            "subject": (
                "AI Operations Agent Notification"
            ),
            "html": f"""
            <div>
                <h2>AI Operations Agent</h2>
                <p>{content}</p>
            </div>
            """
        }

        resend.Emails.send(params)

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