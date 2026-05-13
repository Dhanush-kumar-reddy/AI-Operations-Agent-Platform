from fastapi import FastAPI

from agent import run_agent

from database import SessionLocal, Contact

app = FastAPI()

SUPPORTED_TASKS = {
    "schedule_meeting": "Schedule meetings",
    "send_email": "Send emails"
}


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "AI Agent is running"
    }


# =========================
# RUN AGENT
# =========================

@app.post("/run")
def run(input_text: str):

    result = run_agent(input_text)

    return result


# =========================
# TASKS
# =========================

@app.get("/tasks")
def get_tasks():

    return {
        "supported_tasks": SUPPORTED_TASKS
    }


# =========================
# GET CONTACTS
# =========================

@app.get("/contacts")
def get_contacts():

    db = SessionLocal()

    contacts = db.query(Contact).all()

    db.close()

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


# =========================
# ADD CONTACT
# =========================

@app.post("/contacts")
def add_contact(name: str, email: str):

    db = SessionLocal()

    existing = db.query(Contact).filter(
        Contact.name.ilike(name.strip())
    ).first()

    if existing:

        db.close()

        return {
            "message": "Contact already exists"
        }

    contact = Contact(
        name=name.strip(),
        email=email.strip()
    )

    db.add(contact)

    db.commit()

    db.close()

    return {
        "message": "Contact added successfully"
    }


# =========================
# DELETE CONTACT
# =========================

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):

    db = SessionLocal()

    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()

    if not contact:

        db.close()

        return {
            "message": "Contact not found"
        }

    db.delete(contact)

    db.commit()

    db.close()

    return {
        "message": "Contact deleted successfully"
    }