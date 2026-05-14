from typing import (
    TypedDict,
    List,
    Dict
)


class AgentState(TypedDict):

    user_input: str

    plan: Dict

    results: List[str]

    status: str

    metrics: Dict

    execution_time_seconds: float