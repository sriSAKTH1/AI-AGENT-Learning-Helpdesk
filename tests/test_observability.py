from monitoring.observability import create_run_record


def test_run_record():
    record = create_run_record(
        thread_id="test_thread",
        user_id="test_user",
        question="What is RAG?",
        scope="AI",
        route="rag",
        model_calls=1,
        tool_calls=0,
        confidence=0.90,
        needs_human=False,
    )

    assert record["thread_id"] == "test_thread"
    assert record["scope"] == "AI"
    assert record["route"] == "rag"
    assert record["model_calls"] == 1
    assert record["confidence"] == 0.90


def test_human_escalation_record():
    record = create_run_record(
        thread_id="thread_2",
        user_id="user_2",
        question="Unknown AI question",
        scope="AI",
        route="mentor",
        model_calls=1,
        confidence=0.40,
        needs_human=True,
    )

    assert record["needs_human"] is True
    assert record["route"] == "mentor"