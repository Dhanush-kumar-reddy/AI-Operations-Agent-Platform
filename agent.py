import time
import asyncio

from langsmith import traceable

from langgraph.graph import StateGraph

from models import AgentState

from planner import plan_task

from tools import (
    schedule_meeting,
    send_email
)

from logger import (
    log_step,
    log_error
)

from database import (
    SessionLocal,
    RequestHistory
)


# =========================
# TOOL REGISTRY
# =========================

TOOLS = {
    "schedule_meeting": schedule_meeting,
    "send_email": send_email
}


# =========================
# PLANNER NODE
# =========================

@traceable(name="planner_node")
async def planner_node(state: AgentState):

    try:

        user_input = state.get(
            "user_input",
            ""
        )

        log_step(
            "INPUT",
            user_input
        )

        plan = await plan_task(
            user_input
        )

        log_step(
            "PLANNER_OUTPUT",
            plan
        )

        return {
            "plan": plan
        }

    except Exception as e:

        log_error(
            "PLANNER_ERROR",
            str(e)
        )

        return {
            "plan": {
                "tasks": [],
                "entities": {}
            }
        }


# =========================
# VALIDATOR NODE
# =========================

@traceable(name="validator_node")
async def validator_node(state: AgentState):

    try:

        plan = state.get(
            "plan",
            {}
        )

        log_step(
            "VALIDATION_INPUT",
            plan
        )

        valid_tasks = set(
            TOOLS.keys()
        )

        tasks = plan.get(
            "tasks",
            []
        )

        entities = plan.get(
            "entities",
            {}
        )

        filtered_tasks = [
            task
            for task in tasks
            if task in valid_tasks
        ]

        validated_plan = {
            "tasks": filtered_tasks,
            "entities": entities
        }

        log_step(
            "VALIDATION_OUTPUT",
            validated_plan
        )

        return {
            "plan": validated_plan
        }

    except Exception as e:

        log_error(
            "VALIDATOR_ERROR",
            str(e)
        )

        return {
            "plan": {
                "tasks": [],
                "entities": {}
            }
        }


# =========================
# NO ACTION NODE
# =========================

async def no_action_node(state: AgentState):

    log_step(
        "NO_ACTION",
        state.get("user_input")
    )

    return {
        "results": [],
        "status": "no_action",
        "metrics": {
            "success": 0,
            "failure": 0
        },
        "execution_time_seconds": 0
    }


# =========================
# EXECUTOR NODE
# =========================

@traceable(name="executor_node")
async def executor_node(state: AgentState):

    tasks = state.get(
        "plan",
        {}
    ).get(
        "tasks",
        []
    )

    entities = state.get(
        "plan",
        {}
    ).get(
        "entities",
        {}
    )

    results = []

    start_time = time.time()

    log_step(
        "EXECUTION_START",
        state.get("plan")
    )

    for task in tasks:

        retry = 0

        success = False

        while retry < 2 and not success:

            try:

                tool_fn = TOOLS.get(task)

                if not tool_fn:

                    raise Exception(
                        "Invalid tool"
                    )

                # =========================
                # EXECUTE TOOL
                # =========================

                if task == "schedule_meeting":

                    result = await asyncio.to_thread(
                        tool_fn,
                        entities.get("person"),
                        entities.get("time")
                    )

                    results.append(result)

                    log_step(
                        "TASK_SUCCESS_schedule_meeting",
                        result
                    )

                    # =========================
                    # WORKFLOW CHAINING
                    # =========================

                    confirmation_result = (
                        await asyncio.to_thread(
                            send_email,
                            entities.get("person"),
                            (
                                "Your meeting has been "
                                "scheduled successfully."
                            )
                        )
                    )

                    results.append(
                        confirmation_result
                    )

                    log_step(
                        "CONFIRMATION_EMAIL",
                        confirmation_result
                    )

                elif task == "send_email":

                    result = await asyncio.to_thread(
                        tool_fn,
                        entities.get("person"),
                        "Meeting agenda"
                    )

                    results.append(result)

                    log_step(
                        "TASK_SUCCESS_send_email",
                        result
                    )

                else:

                    result = (
                        f"Failed: "
                        f"Unknown task {task}"
                    )

                    results.append(result)

                # =========================
                # FAILURE DETECTION
                # =========================

                if "failed" in result.lower():

                    log_error(
                        f"{task.upper()}_FAILURE",
                        result
                    )

                success = True

            except Exception as e:

                retry += 1

                log_error(
                    f"{task.upper()}_RETRY_{retry}",
                    str(e)
                )

                if retry == 2:

                    failure_message = (
                        f"Failed: {task}"
                    )

                    results.append(
                        failure_message
                    )

                    log_error(
                        f"{task.upper()}_FINAL_FAILURE",
                        failure_message
                    )

    # =========================
    # METRICS
    # =========================

    success_count = sum(
        1
        for result in results
        if "failed" not in result.lower()
    )

    failure_count = (
        len(results) - success_count
    )

    # =========================
    # STATUS
    # =========================

    if not tasks:

        status = "no_action"

    elif failure_count == 0:

        status = "success"

    elif success_count > 0:

        status = "partial"

    else:

        status = "failed"

    execution_time = round(
        time.time() - start_time,
        2
    )

    log_step(
        "EXECUTION_TIME",
        execution_time
    )

    return {
        "results": results,
        "status": status,
        "metrics": {
            "success": success_count,
            "failure": failure_count
        },
        "execution_time_seconds": execution_time
    }


# =========================
# ROUTING
# =========================

def route(state: AgentState):

    tasks = state.get(
        "plan",
        {}
    ).get(
        "tasks",
        []
    )

    if not tasks:

        return "no_action"

    return "executor"


# =========================
# BUILD GRAPH
# =========================

def build_graph():

    graph = StateGraph(
        AgentState
    )

    graph.add_node(
        "planner",
        planner_node
    )

    graph.add_node(
        "validator",
        validator_node
    )

    graph.add_node(
        "executor",
        executor_node
    )

    graph.add_node(
        "no_action",
        no_action_node
    )

    graph.set_entry_point(
        "planner"
    )

    graph.add_edge(
        "planner",
        "validator"
    )

    graph.add_conditional_edges(
        "validator",
        route,
        {
            "executor": "executor",
            "no_action": "no_action"
        }
    )

    return graph.compile()


# =========================
# RUN AGENT
# =========================

@traceable(name="run_agent")
async def run_agent(user_input: str):

    db = SessionLocal()

    try:

        app = build_graph()

        result = await app.ainvoke({
            "user_input": user_input,
            "plan": {},
            "results": [],
            "status": "",
            "metrics": {},
            "execution_time_seconds": 0
        })

        # =========================
        # STORE HISTORY
        # =========================

        history = RequestHistory(
            user_input=user_input,

            plan=str(
                result.get("plan")
            ),

            results=str(
                result.get("results")
            ),

            status=result.get(
                "status"
            ),

            success_count=result.get(
                "metrics",
                {}
            ).get(
                "success",
                0
            ),

            failure_count=result.get(
                "metrics",
                {}
            ).get(
                "failure",
                0
            ),

            execution_time=result.get(
                "execution_time_seconds",
                0
            )
        )

        db.add(history)

        db.commit()

        return result

    except Exception as e:

        log_error(
            "AGENT_FATAL",
            str(e)
        )

        return {
            "status": "failed",
            "error": "Agent execution failed",
            "details": str(e)
        }

    finally:

        db.close()


# =========================
# LOCAL TESTING
# =========================

if __name__ == "__main__":

    async def test():

        print(
            await run_agent(
                "Schedule a meeting with Rahul tomorrow"
            )
        )

        print(
            await run_agent(
                "Send email to Akash"
            )
        )

        print(
            await run_agent(
                "Do something random"
            )
        )

    asyncio.run(test())