from langgraph.graph import MessagesState
from typing_extensions import TypedDict


class InputState(MessagesState):
    request: str


class State(TypedDict):
    request: str
    response: str
    json_schema: dict
    description: str
    request_step: str


class OutputState(TypedDict):
    response: str
    json_schema: dict
    request_step: str
