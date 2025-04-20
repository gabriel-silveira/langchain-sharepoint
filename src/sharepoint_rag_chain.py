from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from src.database import milvus_host, milvus_port, milvus_collection


class SharePointRAG:
    def __init__(self, username: str):
        self.__host = milvus_host
        self.__port = milvus_port
        self.__collection = milvus_collection

        self.__username = username if username != '' else 'Você'

    def start(self):
        # 1. Embeddings
        embeddings = OpenAIEmbeddings()

        # 2. Conexão com Milvus (certifique-se de que o container esteja ativo)
        vectorstore = Milvus(
            embedding_function=embeddings,
            collection_name=self.__collection,
            connection_args={
                "host": self.__host,
                "port": self.__port,
            },
        )

        # 3. Memória para manter o histórico do chat
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # 4. LLM da OpenAI
        llm = ChatOpenAI(temperature=0)

        # 5. Pipeline RAG com contexto
        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
        )

        # 6. Loop de interação com o usuário
        print(f"Bem-vindo, {self.__username}! 🧠 Chat RAG iniciado. O que você deseja saber?")
        while True:
            query = input(f"\n{self.__username}: ")
            if query.lower() in ("sair", "exit", "quit"):
                break

            result = rag_chain.invoke({"question": query})

            print("\n🤖 Resposta:", result["answer"])
