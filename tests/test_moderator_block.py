import asyncio

from langgraph.types import Command

from backend.app_graph import runtime
from agents.blocking import (
    is_user_blocked,
    unblock_user,
)


async def main():

    user_id = "moderator_test_user"
    thread_id = "moderator_test_001"

    # Clean previous test
    unblock_user(user_id)

    await runtime.startup()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("\n--- STEP 1: OUT-OF-SCOPE QUESTION ---\n")

    result = await runtime.graph.ainvoke(
        {
            "user_id": user_id,
            "thread_id": thread_id,
            "question": "What is today's weather?",
        },
        config=config,
    )

    print(result)

    if "__interrupt__" not in result:

        print(
            "\nERROR: Moderator interrupt "
            "was not triggered."
        )

        await runtime.shutdown()
        return

    print(
        "\nMODERATOR REVIEW REQUIRED."
    )

    print("\n--- STEP 2: MODERATOR BLOCKS USER ---\n")

    result = await runtime.graph.ainvoke(
        Command(resume="block"),
        config=config,
    )

    print(result)

    print(
        "\nBLOCKED:",
        is_user_blocked(user_id),
    )

    await runtime.shutdown()


if __name__ == "__main__":
    asyncio.run(main())