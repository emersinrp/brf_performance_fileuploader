from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_new_token_ygg():
    url = os.environ["AUTH_YGG_QAS"]
    payload = {
        'grant_type': 'client_credentials',
        'client_id': 'operation',
        'client_secret': os.environ["AUTH_YGG_CLIENT_SECRET_BODY"],
        'scope': 'openid'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'client_id': 'financial',
        'client_secret': os.environ["AUTH_YGG_CLIENT_SECRET_HEADER"],
        'Cookie': 'visid_incap_2849035=kxgVA4uDTI+ZucI9a3Dud+LOa2QAAAAAQUIPAAAAAACLiw8529l1QAxwv6n1/vyZ; '
                  'visid_incap_2927240=kXxG8zS3QHWHS6LYFBPLyCUji2QAAAAAQUIPAAAAAACCPFSv9P7NvxrlrjlZUUEw'
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token'], token_data['expires_in']
    else:
        raise Exception(f"Failed to get new token: {response.status_code} {response.text}")


# Atualiza os tokens
def refresh_tokens():
    auth_token, auth_token_expiry = get_authentication()
    new_token, new_token_expiry = get_new_token_ygg()
    return auth_token, auth_token_expiry, new_token, datetime.utcnow() + timedelta(seconds=new_token_expiry)


# Função que verifica a expiração dos tokens e os renova se necessário
def check_token_expiry(auth_token_expiry, auth_token, new_token_expiry, new_token):
    auth_token_expiry_time = datetime.strptime(auth_token_expiry, "%Y-%m-%dT%H:%M:%S.%f") - timedelta(seconds=180)
    if datetime.utcnow() > auth_token_expiry_time or datetime.utcnow() > new_token_expiry:
        auth_token, auth_token_expiry, new_token, new_token_expiry = refresh_tokens()
        return auth_token_expiry, auth_token, new_token_expiry, new_token
    else:
        return auth_token_expiry, auth_token, new_token_expiry, new_token


# Função que gera o token do file uploader
def get_authentication():
    url = os.environ["AUTH_FILEUPLOADER_QAS"]
    new_token, _ = get_new_token_ygg()  # Obtenha o novo token para o header 'Authorization'
    headers = {
        'vendor-id': 'fileuploader-ygg-rvv',
        'Accept': 'application/json',
        'Authorization': f'Bearer {new_token}'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        resposta = response.json()
        return resposta["token"], resposta["expire_at"]
    else:
        raise Exception(f"Failed to authenticate: {response.status_code} {response.text}")
