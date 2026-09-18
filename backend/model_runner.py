import asyncio

from backend.config import MAX_MODEL_CALLS
from backend.model import primary_model, fallback_model


RETRY_ATTEMPTS = 2


def is_retryable_error(error: Exception) -> bool:

    message = str(error).lower()

    retryable_patterns = [
        "429",
        "resource_exhausted",
        "500",
        "502",
        "503",
        "504",
        "temporarily unavailable",
        "timeout",
        "timed out",
    ]

    return any(
        pattern in message
        for pattern in retryable_patterns
    )


def is_quota_error(error: Exception) -> bool:

    message = str(error).lower()

    return (
        "429" in message
        or "resource_exhausted" in message
        or "quota exceeded" in message
        or "generaterequestsperdayperproject" in message
    )


async def invoke_with_fallback(
    prompt: str,
    state: dict | None = None,
):

    state = state or {}

    model_calls = state.get("model_calls", 0)

    last_error = None

    # Primary model
    for attempt in range(RETRY_ATTEMPTS):

        if model_calls >= MAX_MODEL_CALLS:
            raise RuntimeError(
                "Maximum model call limit reached."
            )

        try:

            model_calls += 1

            response = await primary_model.ainvoke(
                prompt
            )

            return response, model_calls

        except Exception as error:

            last_error = error

            print(
                f"Primary model failed "
                f"(attempt {attempt + 1}): {error}"
            )

            if is_quota_error(error):
                print(
                    "Quota error detected. "
                    "Skipping retry and fallback."
                )
                raise error

            if not is_retryable_error(error):
                print(
                    "Non-retryable error detected."
                )
                raise error

            if attempt < RETRY_ATTEMPTS - 1:

                await asyncio.sleep(2)

    # Fallback model
    if model_calls >= MAX_MODEL_CALLS:
        raise RuntimeError(
            "Maximum model call limit reached."
        )

    try:

        model_calls += 1

        response = await fallback_model.ainvoke(
            prompt
        )

        return response, model_calls

    except Exception as error:

        print(f"Fallback model failed: {error}")

        raise last_error
