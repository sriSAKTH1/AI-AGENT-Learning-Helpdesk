from langchain_chroma import Chroma

from rag.embeddings import get_embeddings
from rag.vectorstore import VECTOR_DB_DIR


def get_retriever():
    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name="ai_learning_knowledge",
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )


async def search_knowledge(question: str):
    retriever = get_retriever()

    documents = await retriever.ainvoke(question)

    return documents


if __name__ == "__main__":
    import asyncio

    async def test():
        docs = await search_knowledge(
            "What is LangGraph?"
        )

        print("\nRetrieved documents:\n")

        for doc in docs:
            print(
                "SOURCE:",
                doc.metadata.get("source")
            )
            print(
                doc.page_content[:500]
            )
            print("-" * 60)

    asyncio.run(test())