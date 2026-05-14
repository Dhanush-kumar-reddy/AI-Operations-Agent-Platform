from fastapi import FastAPI

from agent import run_agent

from database import (
    SessionLocal,
    Contact,
    Meeting
)

app = FastAPI()

SUPPORTED_TASKS = {
    "schedule_meeting": "Schedule meetings",
    "send_email": "Send emails"
}


# =========================
# HOME
# =========================

@app.get("/")
async def home():

    return {
        "message": "AI Agent is running"
    }


# =========================
# RUN AGENT
# =========================

@app.post("/run")
async def run(input_text: str):

    print("RUN ENDPOINT HIT")

    try:

        print("CALLING AGENT")

        # IMPORTANT FIX
        result = run_agent(input_text)

        print("AGENT FINISHED")

        return result

    except Exception as e:

        print("RUN ERROR:", str(e))

        return {
            "status": "failed",
            "message": str(e)
        }


# =========================
# TASKS
# =========================

@app.get("/tasks")
async def get_tasks():

    return {
        "supported_tasks": SUPPORTED_TASKS
    }


# =========================
# GET CONTACTS
# =========================

@app.get("/contacts")
async def get_contacts():

    db = SessionLocal()

    try:

        contacts = db.query(Contact).all()

        return {
            "contacts": [
                {
                    "id": c.id,
                    "name": c.name,
                    "email": c.email
                }
                for c in contacts
            ]
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }

    finally:

        db.close()


# =========================
# ADD CONTACT
# =========================

@app.post("/contacts")
async def add_contact(
    name: str,
    email: str
):

    db = SessionLocal()

    try:

        normalized_name = (
            name.strip().lower()
        )

        normalized_email = (
            email.strip().lower()
        )

        if "@" not in normalized_email:

            return {
                "status": "failed",
                "message": "Invalid email address"
            }

        existing = db.query(Contact).filter(
            Contact.name.ilike(
                normalized_name
            )
        ).first()

        if existing:

            return {
                "status": "failed",
                "message": "Contact already exists"
            }

        contact = Contact(
            name=normalized_name,
            email=normalized_email
        )

        db.add(contact)

        db.commit()

        return {
            "status": "success",
            "message": "Contact added successfully"
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }

    finally:

        db.close()


# =========================
# DELETE CONTACT
# =========================

@app.delete("/contacts/{contact_id}")
async def delete_contact(
    contact_id: int
):

    db = SessionLocal()

    try:

        contact = db.query(Contact).filter(
            Contact.id == contact_id
        ).first()

        if not contact:

            return {
                "status": "failed",
                "message": "Contact not found"
            }

        db.delete(contact)

        db.commit()

        return {
            "status": "success",
            "message": "Contact deleted successfully"
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }

    finally:

        db.close()


# =========================
# GET MEETINGS
# =========================

@app.get("/meetings")
async def get_meetings():

    db = SessionLocal()

    try:

        meetings = db.query(
            Meeting
        ).all()

        return {
            "meetings": [
                {
                    "id": m.id,
                    "person": m.person,
                    "time": m.time
                }
                for m in meetings
            ]
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }

    finally:

        db.close()