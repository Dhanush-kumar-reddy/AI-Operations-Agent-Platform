from database import SessionLocal, RequestHistory

db = SessionLocal()

history = db.query(RequestHistory).all()

for h in history:
    print("\n--- REQUEST ---")
    print("Input:", h.user_input)
    print("Plan:", h.plan)
    print("Results:", h.results)
    print("Status:", h.status)
    print("Success:", h.success_count)
    print("Failure:", h.failure_count)
    print("Execution Time:", h.execution_time)

db.close()