from typing import List
from langchain_docling import DoclingLoader
from langchain.schema import Document


def load_documents_with_docling(paths: List[str]) -> List[Document]:
    loader = DoclingLoader(paths)

    documents: List[Document] = loader.load()

    print(f"Documents loaded via Docling: {len(documents)}")

    for d in documents:
        print(d.metadata["source"], "— size:", len(d.page_content))

    return documents
