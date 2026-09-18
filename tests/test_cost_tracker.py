from monitoring.cost_tracker import (
    estimate_cost,
    create_usage_record,
)


def test_zero_cost():
    cost = estimate_cost(
        input_tokens=0,
        output_tokens=0,
    )

    assert cost == 0.0


def test_cost_calculation():
    cost = estimate_cost(
        input_tokens=1_000_000,
        output_tokens=500_000,
        input_price_per_million=1.0,
        output_price_per_million=2.0,
    )

    assert cost == 2.0


def test_usage_record():
    record = create_usage_record(
        model="gemini-3.6-flash",
        input_tokens=100,
        output_tokens=50,
        model_calls=1,
        tool_calls=2,
    )

    assert record["total_tokens"] == 150
    assert record["model_calls"] == 1
    assert record["tool_calls"] == 2
