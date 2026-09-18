from tavily import AsyncTavilyClient

from backend.config import TAVILY_API_KEY


client = AsyncTavilyClient(api_key=TAVILY_API_KEY)


async def web_search(query: str, max_results: int = 3):
    results = await client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=True,
    )

    return results