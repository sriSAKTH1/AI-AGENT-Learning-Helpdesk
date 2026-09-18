from typing import TypedDict


class AgentState(TypedDict, total=False):

    user_id: str
    thread_id: str
    question: str

    scope: str
    route: str

    retrieved_docs: list
    web_sources: list

    answer: str
    confidence: float

    citations: list[str]
    learning_resources: list[str]

    needs_human: bool
    escalation_reason: str | None

    blocked: bool
    unblocked: bool

    security_blocked: bool
    security_reason: str | None

    model_calls: int
    tool_calls: int

    approval_required: bool
    approval_status: str | None
    support_ticket_id: str | None

    moderator_action: str | None