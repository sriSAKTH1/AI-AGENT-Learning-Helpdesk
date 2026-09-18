import pytest

from backend.graph import (
    check_scope,
    route_scope,
    is_unblock_request,
)


@pytest.mark.asyncio
async def test_ai_scope():
    state = {
        "question": "Explain LangGraph"
    }

    result = await check_scope(state)

    assert result["scope"] == "AI"


@pytest.mark.asyncio
async def test_rag_question():
    state = {
        "question": "What is Agentic RAG?"
    }

    result = await check_scope(state)

    assert result["scope"] == "AI"
    assert route_scope({
        **state,
        **result,
    }) == "rag"


@pytest.mark.asyncio
async def test_latest_ai_question_goes_web():
    state = {
        "question": "What is the latest LangGraph release?"
    }

    result = await check_scope(state)

    assert result["scope"] == "AI"
    assert route_scope({
        **state,
        **result,
    }) == "web"


@pytest.mark.asyncio
async def test_weather_is_out_of_scope():
    state = {
        "question": "What is today's weather?"
    }

    result = await check_scope(state)

    assert result["scope"] == "OUT_OF_SCOPE"

    assert route_scope({
        **state,
        **result,
    }) == "moderator"


@pytest.mark.asyncio
async def test_recipe_is_out_of_scope():
    state = {
        "question": "Give me a chicken recipe"
    }

    result = await check_scope(state)

    assert result["scope"] == "OUT_OF_SCOPE"


@pytest.mark.asyncio
async def test_cricket_is_out_of_scope():
    state = {
        "question": "Who won today's cricket match?"
    }

    result = await check_scope(state)

    assert result["scope"] == "OUT_OF_SCOPE"


def test_unblock_messages():

    assert is_unblock_request(
        "sorry"
    )

    assert is_unblock_request(
        "I am sorry"
    )

    assert is_unblock_request(
        "I'm sorry"
    )

    assert is_unblock_request(
        "please unblock me"
    )

    assert is_unblock_request(
        "unblock me"
    )


def test_normal_message_is_not_unblock():

    assert not is_unblock_request(
        "Explain LangGraph"
    )