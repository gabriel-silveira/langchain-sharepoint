from dotenv import dotenv_values
from pymilvus import Collection, MilvusException, connections, db, utility
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

config = dotenv_values(".env")

milvus_host = config['MILVUS_HOST']
milvus_port = config['MILVUS_PORT']
milvus_collection = config['MILVUS_COLLECTION']

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
        collection_name=milvus_collection
    )


def similarity_search(query: str):
    vectorstore = Milvus(
        embedding_function=embeddings,
        collection_name=milvus_collection,
        connection_args={
            "host": milvus_host,
            "port": milvus_port,
        },
    )

    results = vectorstore.similarity_search(query, k=3)

    # serialized = "\n\n".join(
    #     f"Source: {doc.metadata}\n" f"Content: {doc.page_content}"
    #     for doc in results
    # )
    # return serialized, results

    return results


def create_database():
    # Check if the database exists
    try:
        existing_databases = db.list_database()

        if milvus_collection in existing_databases:
            print(f"Database '{milvus_collection}' already exists.")

            # Use the database context
            db.using_database(milvus_collection)

            # Drop all collections in the database
            collections = utility.list_collections()

            for collection_name in collections:
                collection = Collection(name=collection_name)
                collection.drop()
                print(f"Collection '{collection_name}' has been dropped.")

            db.drop_database(milvus_collection)

            print(f"Database '{milvus_collection}' has been deleted.")
        else:
            print(f"Database '{milvus_collection}' does not exist.")

            database = db.create_database(milvus_collection)

            print(f"Database '{milvus_collection}' created successfully.")
    except MilvusException as e:
        print(f"An error occurred: {e}")
