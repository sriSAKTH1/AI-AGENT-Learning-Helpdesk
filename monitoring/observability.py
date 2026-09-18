from datetime import datetime, timezone


def create_run_record(
    thread_id: str,
    user_id: str,
    question: str,
    scope: str = "",
    route: str = "",
    model_calls: int = 0,
    tool_calls: int = 0,
    confidence: float = 0.0,
    needs_human: bool = False,
):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "thread_id": thread_id,
        "user_id": user_id,
        "question": question,
        "scope": scope,
        "route": route,
        "model_calls": model_calls,
        "tool_calls": tool_calls,
        "confidence": confidence,
        "needs_human": needs_human,
    }