from pathlib import Path

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loader import load_markdown_documents
from rag.embeddings import get_embeddings


VECTOR_DB_DIR = Path(__file__).resolve().parent.parent / "chroma_db"


def create_vectorstore():
    documents = load_markdown_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    print(f"Loaded documents : {len(documents)}")
    print(f"Created chunks   : {len(chunks)}")

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
        collection_name="ai_learning_knowledge",
    )

    print(f"Vector database created: {VECTOR_DB_DIR}")

    return vectorstore


if __name__ == "__main__":
    create_vectorstore()