from pydantic import BaseModel, Field


class AgentResponse(BaseModel):

    answer: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    scope: str

    citations: list[str] = []

    web_sources: list[str] = []

    learning_resources: list[str] = []

    needs_human: bool = False

    escalation_reason: str | None = None

    action_required: bool = False