import asyncio

from backend.model import model


async def main():
    response = await model.ainvoke(
        "What is an AI agent? Answer in one sentence."
    )

    print("\nAI RESPONSE:")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())