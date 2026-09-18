import asyncio

from backend.app_graph import runtime
from agents.blocking import block_user, unblock_user


async def main():

    user_id = "blocked_request_test"
    thread_id = "blocked_request_001"

    unblock_user(user_id)
    block_user(user_id)

    await runtime.startup()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("\n--- BLOCKED USER REQUEST TEST ---\n")

    result = await runtime.graph.ainvoke(
        {
            "user_id": user_id,
            "thread_id": thread_id,
            "question": "Explain LangGraph",
        },
        config=config,
    )

    print(result)

    assert result["blocked"] is True
    assert "temporarily blocked" in result["answer"]

    print("\n✅ BLOCKED USER STOPPED BEFORE AI PROCESSING")

    unblock_user(user_id)

    await runtime.shutdown()


if __name__ == "__main__":
    asyncio.run(main())