from typing import List
import requests


def rea(url: str, file_path: str):
    response = requests.get(url)

    if file_path != "":
        with open(file_path, "wb") as f:
            f.write(response.content)


def write_docs_locally(files: dict) -> List[str] | None:
    docs = []

    try:
        if "value" in files:
            for file in files["value"]:
                if "@microsoft.graph.downloadUrl" in file and "name" in file:
                    response = requests.get(file['@microsoft.graph.downloadUrl'])

                    file_path = f"files/{file["name"]}"

                    with open(file_path, "wb") as f:
                        f.write(response.content)

                        docs.append(file_path)

        return docs
    except Exception as e:
        print(e)
