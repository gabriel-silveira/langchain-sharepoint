from msal import PublicClientApplication
from msal import ConfidentialClientApplication
from dotenv import dotenv_values

config = dotenv_values(".env")

client_id = config['CLIENT_ID']
tenant_id = config['TENANT_ID']
client_secret = config['CLIENT_SECRET']


def get_token():
  authority = f"https://login.microsoftonline.com/{tenant_id}"
  scope = ["https://graph.microsoft.com/.default"]

  app = PublicClientApplication(client_id=client_id, authority=authority)

  result = app.acquire_token_interactive(scopes=scope)

  print("Result\n")
  print(result)

  return result['access_token']


def get_confidential_token():
  authority = f"https://login.microsoftonline.com/{tenant_id}"
  scope = ["https://graph.microsoft.com/.default"]

  app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
  )

  result = app.acquire_token_for_client(scopes=scope)

  print("Result\n")
  print(result)

  return result['access_token']
