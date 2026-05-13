from langsmith import traceable
from langgraph.graph import StateGraph
from models import AgentState
from planner import plan_task
from tools import schedule_meeting, send_email
from logger import log_step, log_error
import time
from database import (
    SessionLocal,
    RequestHistory
)

# Tool registry (IMPORTANT UPGRADE)
TOOLS = {
    "schedule_meeting": schedule_meeting,
    "send_email": send_email
}


# 🔹 Planner Node
@traceable(name="planner_node")
def planner_node(state: AgentState):
    try:
        log_step("INPUT", state["user_input"])

        plan = plan_task(state["user_input"])

        log_step("PLANNER_OUTPUT", plan)

        return {"plan": plan}

    except Exception as e:
        log_error("PLANNER", str(e))
        return {"plan": {"tasks": [], "entities": {}}}


# 🔹 Validator Node
@traceable(name="validator_node")
def validator_node(state: AgentState):
    try:
        plan = state.get("plan", {})
        log_step("VALIDATION_INPUT", plan)

        valid_tasks = set(TOOLS.keys())

        tasks = plan.get("tasks", [])
        entities = plan.get("entities", {})

        filtered_tasks = [t for t in tasks if t in valid_tasks]

        validated_plan = {
            "tasks": filtered_tasks,
            "entities": entities
        }

        log_step("VALIDATION_OUTPUT", validated_plan)

        return {"plan": validated_plan}

    except Exception as e:
        log_error("VALIDATOR", str(e))
        return {"plan": {"tasks": [], "entities": {}}}

def no_action_node(state: AgentState):
    return {
        "results": [],

        "status": "no_action",

        "metrics": {
            "success": 0,
            "failure": 0
        },

        "execution_time_seconds": 0
    }
    
    
# 🔹 Executor Node
@traceable(name="executor_node")
def executor_node(state: AgentState):
    tasks = state["plan"].get("tasks", [])
    entities = state["plan"].get("entities", {})

    results = []
    start_time = time.time()

    log_step("EXECUTION_START", state["plan"])

    for task in tasks:
        retry = 0
        success = False

        while retry < 2 and not success:
            try:
                tool_fn = TOOLS.get(task)

                if not tool_fn:
                    raise Exception("Invalid tool")

                # ✅ Execute correct tool
                if task == "schedule_meeting":
                    result = tool_fn(
                        entities.get("person"),
                        entities.get("time")
                    )

                elif task == "send_email":
                    result = tool_fn(
                        entities.get("person"),
                        "Meeting agenda"
                    )

                else:
                    result = f"Failed: Unknown task {task}"

                # ✅ Detect logical failures
                if "failed" in result.lower():
                    log_error(f"{task.upper()}_FAILURE", result)

                else:
                    log_step(f"TASK_SUCCESS_{task}", result)

                # ✅ Store result
                results.append(result)

                success = True

            except Exception as e:
                retry += 1

                log_error(f"TASK_FAIL_{task}", str(e))

                if retry == 2:
                    failure_message = f"Failed: {task}"

                    results.append(failure_message)

                    log_error(
                        f"{task.upper()}_FINAL_FAILURE",
                        failure_message
                    )

    log_step("EXECUTION_RESULT", results)

    # ✅ Metrics
    success_count = sum(
        1 for r in results if "failed" not in r.lower()
    )

    failure_count = len(results) - success_count

    # ✅ Status
    status = "success"

    if failure_count > 0:
        status = (
            "partial"
            if success_count > 0
            else "failed"
        )

    execution_time = round(
        time.time() - start_time,
        2
    )
    log_step("EXECUTION_TIME", execution_time)
    
    if not tasks:
        status = "no_action"

        success_count = 0
        failure_count = 0
    
    return {
        "results": results,
        "status": status,
        "metrics": {
            "success": success_count,
            "failure": failure_count
        },
        "execution_time_seconds": execution_time
    }

# 🔹 Routing
def route(state: AgentState):
    if not state["plan"].get("tasks"):
        return "no_action"

    return "executor"


# 🔹 Graph
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("no_action", no_action_node)
    graph.add_node("planner", planner_node)
    graph.add_node("validator", validator_node)
    graph.add_node("executor", executor_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "validator")

    graph.add_conditional_edges(
        "validator",
        route,
        {
            "executor": "executor",
            "no_action": "no_action"
        }
    )

    return graph.compile()


# 🔹 Run Agent
@traceable(name="run_agent")
def run_agent(user_input: str):
    try:
        app = build_graph()

        # ✅ Run graph
        result = app.invoke({
            "user_input": user_input,

            "plan": {},

            "results": [],

            "status": "",

            "metrics": {},

            "execution_time_seconds": 0
        })

        # Save request history
        db = SessionLocal()

        history = RequestHistory(
            user_input=user_input,

            plan=str(result.get("plan")),

            results=str(result.get("results")),

            status=result.get("status"),

            success_count=result.get(
                "metrics", {}
            ).get("success", 0),

            failure_count=result.get(
                "metrics", {}
            ).get("failure", 0),

            execution_time=str(
                result.get(
                    "execution_time_seconds", 0
                )
            )
        )

        db.add(history)

        db.commit()

        db.close()

        return result

    except Exception as e:
        log_error("AGENT_FATAL", str(e))

        return {
            "error": "Agent execution failed",
            "details": str(e)
        }


# 🔹 Testing
if __name__ == "__main__":
    print(run_agent("Schedule a meeting with Rahul tomorrow"))
    print(run_agent("Send email to Akash"))
    print(run_agent("Do something random"))