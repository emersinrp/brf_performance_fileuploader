from datetime import datetime, timedelta

import pytz
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

token_expiry = None  # Inicializando com um valor menor que o tempo atual
expiry_token_qas = token_expiry


def refresh_token():
    print("ESTA PASSANDO AQUI")
    auth, token_expiry = get_authentication()  # Obtendo um novo token
    print("AUTORIZATHION QAS: ", auth, token_expiry)

    return auth, token_expiry


def check_token_expiry(token_expiry, token):
    print("TOKEN EXPIRY: ", datetime.strptime(token_expiry, "%Y-%m-%dT%H:%M:%S.%f"))
    print("TIME TIME: ", datetime.utcnow())
    if datetime.now() > datetime.strptime(token_expiry, "%Y-%m-%dT%H:%M:%S.%f"):
        new_token, expiry_token_qas = refresh_token()  # Renova o token se tiver expirado

        print("TEM QUE ENTRAR AQUI: ", expiry_token_qas)
    else:
        new_token = token
        expiry_token_qas = token_expiry

    return expiry_token_qas, new_token


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

    return f'{resposta["token"]}', f'{resposta["expire_at"]}'
