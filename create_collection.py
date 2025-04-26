from src.milvus import create_collection

if __name__ == "__main__":
    my_collection_name = input("Digite o nome da collection que deseja criar:\n")

    answer = input(f"O nome da collection \"{my_collection_name}\" está correto? (s/n)\n")

    if answer.lower() == 's':
        create_collection(my_collection_name)
