import asyncio

from langgraph.types import Command

from backend.app_graph import runtime


async def main():

    await runtime.startup()

    config = {
    "configurable": {
        "thread_id": "hitl_test_002"
    }
}

    print("\n--- STEP 1: START GRAPH ---\n")

    result = await runtime.graph.ainvoke(
    {
        "user_id": "learner_001",
        "thread_id": "hitl_test_002",
        "question": "What is LangGraph?",
    },
    config=config,
    )

    print("GRAPH RESULT:")
    print(result)

    print("\n--- STEP 2: CHECK INTERRUPT ---\n")

    if "__interrupt__" in result:

        print("GRAPH PAUSED FOR HUMAN APPROVAL.")

        print("\nINTERRUPT DATA:")

        for interrupt_data in result["__interrupt__"]:
            print(interrupt_data)

    else:

        print("ERROR: Graph did not pause.")

        await runtime.shutdown()
        return

    print("\n--- STEP 3: HUMAN APPROVES ---\n")

    resumed_result = await runtime.graph.ainvoke(
        Command(resume="approve"),
        config=config,
    )

    print("RESUMED RESULT:")
    print(resumed_result)

    await runtime.shutdown()


if __name__ == "__main__":
    asyncio.run(main())