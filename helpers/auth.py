import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

authorization_qas = None
token_expiry = time.time() - 1  # Inicializando com um valor menor que o tempo atual


def refresh_token():
    global authorization_qas
    print("ESTA PASSANDO AQUI")
    authorization_qas = get_authentication()  # Obtendo um novo token
    print("AUTORIZATHION QAS: ", authorization_qas)


def check_token_expiry():
    global token_expiry
    global authorization_qas

    if time.time() > token_expiry:
        refresh_token()  # Renova o token se tiver expirado
        token_expiry = time.time() + 1800  # Atualiza o tempo de validade para 30 minutos à frente


def get_authentication():
    url = "https://ygg-qas.brf.cloud/fileuploader/file_uploader/auth"

    headers = {
        'vendor-id': 'fileuploader-ygg-rvv',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers)
    print("Authentication response status code:", response.status_code)
    print("Authentication response body:", response.text)

    resposta = response.json()

    return f'{resposta["token"]}'
