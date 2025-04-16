import requests


def get_sharepoint_files(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    site_url = "https://graph.microsoft.com/v1.0/sites/verxti.sharepoint.com:/sites/ProspeccaoVERX2025"
    site = requests.get(site_url, headers=headers).json()

    if site:
        site_id = site["id"]

        # Agora pegue os drives (bibliotecas de documentos)
        drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives = requests.get(drives_url, headers=headers).json()

        # Pegue os arquivos de uma pasta específica
        drive_id = drives['value'][0]['id']
        files_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
        files = requests.get(files_url, headers=headers).json()

        return files
    else:
        print('Não foi possível obter arquivos.')
