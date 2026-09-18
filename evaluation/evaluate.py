import json
import asyncio

from backend.app_graph import runtime


QUESTIONS_FILE = "evaluation/questions.json"


async def evaluate():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    print(f"Loaded evaluation questions: {len(questions)}")

    passed = 0
    failed = 0

    for index, item in enumerate(questions, start=1):

        question = item["question"]

        thread_id = f"eval_{index}"

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        try:
            result = await runtime.graph.ainvoke(
                {
                    "user_id": f"eval_user_{index}",
                    "thread_id": thread_id,
                    "question": question,
                },
                config=config,
            )

            actual_scope = result.get("scope")
            expected_scope = item["expected_scope"]

            if actual_scope == expected_scope:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(
                f"[{status}] "
                f"{index:02d} | "
                f"{question} | "
                f"scope={actual_scope}"
            )

        except Exception as error:
            failed += 1

            print(
                f"[ERROR] "
                f"{index:02d} | "
                f"{question} | "
                f"{error}"
            )

    total = passed + failed

    print("\n==============================")
    print("Evaluation Complete")
    print("==============================")
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if total:
        accuracy = (passed / total) * 100
        print(f"Scope Accuracy: {accuracy:.2f}%")

    return passed, failed


async def main():
    await runtime.startup()

    try:
        await evaluate()
    finally:
        await runtime.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
