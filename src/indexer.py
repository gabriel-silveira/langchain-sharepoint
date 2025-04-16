from dotenv import dotenv_values
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

config = dotenv_values(".env")

milvus_host = config['MILVUS_HOST']
milvus_port = config['MILVUS_PORT']


def index_in_milvus(docs: list[Document]):
    embeddings = OpenAIEmbeddings()

    Milvus.from_documents(
        docs,
        embedding=embeddings,
        connection_args={
            "host": milvus_host,
            "port": milvus_port,
        },
        collection_name="docling_docs"
    )
