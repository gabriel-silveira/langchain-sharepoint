from dotenv import dotenv_values
from pymilvus import Collection, MilvusException, connections, db, utility
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

config = dotenv_values(".env")

milvus_host = config['MILVUS_HOST']
milvus_port = config['MILVUS_PORT']

conn = connections.connect(host=milvus_host, port=milvus_port)

embeddings = OpenAIEmbeddings()


def index_in_milvus(docs: list[Document]):
    Milvus.from_documents(
        docs,
        embedding=embeddings,
        connection_args={
            "host": milvus_host,
            "port": milvus_port,
        },
        collection_name="verx_sharepoint"
    )


def similarity_search(query: str):
    vector_store_loaded = Milvus(
        embedding_function=embeddings,
        connection_args={
            "host": milvus_host,
            "port": milvus_port,
        },
        collection_name="langchain_example",
    )

    retrieved_docs = vector_store_loaded.similarity_search(query, k=2)

    serialized = "\n\n".join(
        f"Source: {doc.metadata}\n" f"Content: {doc.page_content}"
        for doc in retrieved_docs
    )

    return serialized, retrieved_docs


def create_database():
    db_name = "verx_sharepoint"

    # Check if the database exists
    try:
        existing_databases = db.list_database()

        if db_name in existing_databases:
            print(f"Database '{db_name}' already exists.")

            # Use the database context
            db.using_database(db_name)

            # Drop all collections in the database
            collections = utility.list_collections()

            for collection_name in collections:
                collection = Collection(name=collection_name)
                collection.drop()
                print(f"Collection '{collection_name}' has been dropped.")

            db.drop_database(db_name)

            print(f"Database '{db_name}' has been deleted.")
        else:
            print(f"Database '{db_name}' does not exist.")

            database = db.create_database(db_name)

            print(f"Database '{db_name}' created successfully.")
    except MilvusException as e:
        print(f"An error occurred: {e}")
