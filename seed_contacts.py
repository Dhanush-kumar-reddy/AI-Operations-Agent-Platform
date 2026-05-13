from database import SessionLocal, Contact

db = SessionLocal()

contacts = [
    Contact(name="Akash", email="akash@gmail.com"),
    Contact(name="Rahul", email="rahul@gmail.com"),
    Contact(name="Dhanush", email="dhanushkumar4211@gmail.com")
]

for contact in contacts:
    existing = db.query(Contact).filter(
        Contact.name == contact.name
    ).first()

    if not existing:
        db.add(contact)

db.commit()
db.close()

print("Contacts added successfully")