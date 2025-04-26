from dotenv import load_dotenv
from src.graph import get_sharepoint_files
from src.auth import get_confidential_token
from src.files import write_docs_locally
from src.docling_loader import load_documents_with_docling
from src.milvus import index_in_milvus

load_dotenv()

if __name__ == "__main__":
    # 1. Get access token to Graph API
    token = get_confidential_token()

    # 2. Retrieve documents from SharePoint
    files = get_sharepoint_files(token)

    # 3. Write files locally
    document_paths = write_docs_locally(files)

    # 4. Load Docling documents
    docling_docs = load_documents_with_docling(document_paths)

    # 5. Index in Milvus vector database
    index_in_milvus(docling_docs)