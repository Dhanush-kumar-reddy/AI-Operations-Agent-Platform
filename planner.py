import os
import json

from dotenv import load_dotenv

from openai import AsyncOpenAI


# =========================
# LOAD ENV
# =========================

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# NORMALIZE PLAN
# =========================

def normalize_plan(plan: dict):

    tasks = plan.get(
        "tasks",
        []
    )

    if (
        tasks
        and isinstance(tasks[0], dict)
    ):

        tasks = [
            task.get("task")
            for task in tasks
            if "task" in task
        ]

    if not isinstance(tasks, list):

        tasks = []

    tasks = [str(task) for task in tasks]

    entities = plan.get(
        "entities",
        {}
    )

    if not isinstance(
        entities,
        dict
    ):

        entities = {}

    return {
        "tasks": tasks,
        "entities": entities
    }


# =========================
# PLAN TASK
# =========================

async def plan_task(user_input: str):

    prompt = f"""
You are an AI planner.

Convert user input into STRICT JSON.

Allowed tasks:
- schedule_meeting
- send_email

Rules:
- tasks MUST be a list of strings
- Always return valid JSON
- No explanations
- If unclear → empty tasks

Output format:

{{
  "tasks": ["task_name"],
  "entities": {{
    "person": "",
    "time": ""
  }}
}}

Input:
{user_input}
"""

    try:

        response = (
            await client.chat.completions.create(
                model="gpt-4o-mini",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        output = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        parsed = json.loads(output)

        return normalize_plan(parsed)

    except Exception as e:

        print(
            "Planner Error:",
            str(e)
        )

        return {
            "tasks": [],
            "entities": {}
        }


# =========================
# TESTING
# =========================

if __name__ == "__main__":

    import asyncio

    print(
        asyncio.run(
            plan_task(
                "Schedule a meeting with Rahul tomorrow"
            )
        )
    )