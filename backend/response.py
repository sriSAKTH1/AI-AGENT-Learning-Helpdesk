from backend.schemas import AgentResponse


def format_agent_response(state):

    citations = state.get("citations", [])
    web_sources = state.get("web_sources", [])

    learning_resources = state.get(
        "learning_resources",
        []
    )

    citations = list(dict.fromkeys(citations))
    web_sources = list(dict.fromkeys(web_sources))
    learning_resources = list(
        dict.fromkeys(learning_resources)
    )

    response = AgentResponse(
        answer=state.get(
            "answer",
            "No answer available."
        ),

        confidence=state.get(
            "confidence",
            0.0
        ),

        scope=state.get(
            "scope",
            "UNKNOWN"
        ),

        citations=citations,

        web_sources=web_sources,

        learning_resources=learning_resources,

        needs_human=state.get(
            "needs_human",
            False
        ),

        escalation_reason=state.get(
            "escalation_reason"
        ),

        action_required=state.get(
            "approval_required",
            False
        ),
    )

    return response.model_dump()