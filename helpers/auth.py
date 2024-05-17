from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()


def refresh_token():  # get a new token
    auth, token_expiry = get_authentication()
    return auth, token_expiry


def check_token_expiry(token_expiry, token):  # validates token expiration
    time_expiry = datetime.strptime(token_expiry, "%Y-%m-%dT%H:%M:%S.%f") - timedelta(seconds=300)
    if datetime.utcnow() > time_expiry:
        new_token, new_token_expiry = refresh_token()  # renew the token if it has expired
        return new_token_expiry, new_token
    else:
        return token_expiry, token


def get_authentication():  # generates the token
    url = "https://ygg-qas.brf.cloud/fileuploader/file_uploader/auth"
    headers = {
        'vendor-id': 'fileuploader-ygg-rvv',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    resposta = response.json()

    return resposta["token"], resposta["expire_at"]
