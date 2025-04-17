from typing import List
from langchain_docling import DoclingLoader
from langchain.schema import Document


def load_documents_with_docling(paths: List[str]) -> List[Document]:
    loader = DoclingLoader(paths)

    documents: List[Document] = loader.load()

    for doc in documents:
        print(doc.metadata["source"], "— size:", len(doc.page_content), "\n")
        print(doc, "\n")

    print(f"Documents loaded via Docling: {len(documents)}\n")

    return documents
