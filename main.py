from dotenv import load_dotenv
from src.graph import get_sharepoint_files
from src.auth import get_confidential_token
from src.files import write_docs_locally
from src.docling_loader import load_documents_with_docling
from src.indexer import index_in_milvus

load_dotenv()

if __name__ == "__main__":
    # 1.
    token = get_confidential_token()

    # 2.
    files = get_sharepoint_files(token)

    # 3.
    document_paths = write_docs_locally(files)

    # 4.
    docling_docs = load_documents_with_docling(document_paths)

    for doc in docling_docs:
        print(doc)

    # 5.
    index_in_milvus(docling_docs)
