import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Normalize LLM output (VERY IMPORTANT)
def normalize_plan(plan: dict):
    tasks = plan.get("tasks", [])

    # Fix if tasks come as objects instead of strings
    if tasks and isinstance(tasks[0], dict):
        tasks = [t.get("task") for t in tasks if "task" in t]

    # Ensure tasks is always a list of strings
    if not isinstance(tasks, list):
        tasks = []

    tasks = [str(t) for t in tasks]

    entities = plan.get("entities", {})

    if not isinstance(entities, dict):
        entities = {}

    return {
        "tasks": tasks,
        "entities": entities
    }


# 🧠 Main planner function
def plan_task(user_input: str):
    prompt = f"""
You are an AI planner.

Convert user input into STRICT JSON.

Allowed tasks:
- schedule_meeting
- send_email

Rules:
- tasks MUST be a list of strings (NOT objects)
- Example: ["schedule_meeting"]
- DO NOT return objects like {{"task": "..."}}
- Always return valid JSON
- Do not include explanations
- If task is unclear → return empty tasks

Output format:
{{
  "tasks": ["task_name"],
  "entities": {{
    "person": "",
    "time": ""
  }}
}}

If no valid task:
{{
  "tasks": [],
  "entities": {{}}
}}

Input:
{user_input}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content.strip()

        # Parse JSON safely
        parsed = json.loads(output)

        # Normalize structure
        return normalize_plan(parsed)

    except Exception as e:
        print("Planner Error:", str(e))

        # Safe fallback
        return {
            "tasks": [],
            "entities": {}
        }


# 🧪 Testing
if __name__ == "__main__":
    print(plan_task("Schedule a meeting with Rahul tomorrow"))
    print(plan_task("Send email to Akash"))
    print(plan_task("Do something random"))