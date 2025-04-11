import requests


def write_file(url: str, name: str):
  response = requests.get(url)

  with open(name, "wb") as f:
    f.write(response.content)
