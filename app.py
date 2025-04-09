from src.graph import get_files
from src.auth import get_confidential_token
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  token = get_confidential_token()

  files = get_files(token)

  print(files)
