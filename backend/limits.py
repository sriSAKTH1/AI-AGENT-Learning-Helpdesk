from backend.config import MAX_MODEL_CALLS, MAX_TOOL_CALLS


def check_model_limit(state):
    calls = state.get("model_calls", 0)

    if calls >= MAX_MODEL_CALLS:
        return False

    return True


def check_tool_limit(state):
    calls = state.get("tool_calls", 0)

    if calls >= MAX_TOOL_CALLS:
        return False

    return True


def increment_model_calls(state):
    return {
        "model_calls": state.get("model_calls", 0) + 1
    }


def increment_tool_calls(state):
    return {
        "tool_calls": state.get("tool_calls", 0) + 1
    }
