from pathlib import Path
from langchain_core.documents import Document


KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_markdown_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "path": str(file_path),
                },
            )
        )

    return documents


if __name__ == "__main__":
    docs = load_markdown_documents()

    print(f"Loaded documents: {len(docs)}")

    for doc in docs:
        print(
            f"{doc.metadata['source']} "
            f"-> {len(doc.page_content)} characters"
        )