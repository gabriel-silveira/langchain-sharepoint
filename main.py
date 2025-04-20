from src.sharepoint_rag_chain import SharePointRAG

if __name__ == "__main__":
    username = input("Olá! Qual é o seu nome?\n")

    rag = SharePointRAG(username)

    rag.start()
