import asyncio

from tools.web_search import web_search


async def main():
    results = await web_search(
        "latest LangGraph documentation"
    )

    print("\nWEB SEARCH RESULTS\n")

    for result in results["results"]:
        print("TITLE:", result["title"])
        print("URL:", result["url"])
        print("CONTENT:", result["content"][:300])
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())