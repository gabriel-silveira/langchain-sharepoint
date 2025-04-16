from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document


def index_in_milvus(docs: list[Document], milvus_host="localhost"):
    embeddings = OpenAIEmbeddings()
    Milvus.from_documents(
        docs,
        embedding=embeddings,
        connection_args={"host": milvus_host, "port": "19530"},
        collection_name="docling_docs"
    )
