from datetime import datetime, timezone


def estimate_cost(
    input_tokens: int = 0,
    output_tokens: int = 0,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> float:
    input_cost = (
        input_tokens / 1_000_000
    ) * input_price_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * output_price_per_million

    return round(input_cost + output_cost, 8)


def create_usage_record(
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    model_calls: int = 1,
    tool_calls: int = 0,
    estimated_cost_usd: float = 0.0,
) -> dict:

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "model": model,

        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,

        "model_calls": model_calls,
        "tool_calls": tool_calls,

        "estimated_cost_usd": estimated_cost_usd,
    }