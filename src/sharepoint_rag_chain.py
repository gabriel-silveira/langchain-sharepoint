from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_milvus import Milvus
from langchain.chains import ConversationalRetrievalChain
from src.milvus import milvus_host, milvus_port, milvus_collection
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Dicionário para simular múltiplos usuários
chat_histories = {}


def get_message_history(session_id: str):
    """Recupera ou cria histórico de mensagens para uma sessão."""
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]


class SharePointRAG:
    def __init__(self, username: str = ''):
        self.__host = milvus_host
        self.__port = milvus_port
        self.__collection = milvus_collection

        self.__username = username if username != '' else 'Você'

    def get_chain(self):
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

        # 4. LLM da OpenAI
        llm = ChatOpenAI(temperature=0)

        # 5. Pipeline RAG com contexto
        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=False,
        )

        # Adiciona histórico de mensagens ao pipeline
        chain_with_history = RunnableWithMessageHistory(
            rag_chain,
            get_message_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

        return chain_with_history

    def start(self):
        rag_chain = self.get_chain()

        # 6. Loop de interação com o usuário
        print(f"Bem-vindo, {self.__username}! 🧠 Chat RAG iniciado. O que você deseja saber?")
        while True:
            query = input(f"\n{self.__username}: ")
            if query.lower() in ("sair", "exit", "quit"):
                break

            result = rag_chain.invoke(
                {"question": query},
                config={"configurable": {"session_id": 'console_session'}}
            )

            print("\n🤖 Resposta:", result["answer"])
