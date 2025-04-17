from src.database import similarity_search

if __name__ == "__main__":
    query = input("Como posso ajudar?\n")

    result = similarity_search(query)

    print(result)
