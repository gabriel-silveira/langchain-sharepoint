from src.graph import get_files
from src.auth import get_confidential_token
from src.loader import write_file
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  token = get_confidential_token()

  files = get_files(token)

  for file in files:
    if file['@microsoft.graph.downloadUrl']:
      write_file(file['@microsoft.graph.downloadUrl'], file['name'])
