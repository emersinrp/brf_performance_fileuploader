import random
import time
from locust import HttpUser, task, between, tag
import os
from dotenv import load_dotenv
from helpers.auth import refresh_token, check_token_expiry
from helpers.rules import prepare_upload_data, handle_response

load_dotenv()
global token_expiry


class PostFileUploader(HttpUser):
    def __int__(self) -> None:
        self.token_expiry = None
        self.authorization_qas = None

    host = os.environ["KONG_FILEUPLOADER_QAS"]
    wait_time = between(1.0, 3.0)
    prefix_fileuploader = os.environ["PREFIX_FILEUPLOADER"]
    LIST_FILES = ["imagens_teste/teste_img_2.jpg"]

    def on_start(self):
        self.authorization_qas, self.token_expiry = refresh_token()  # Chamando o método para obter o token inicial

    @task
    def post_file_uploader(self):
        self.token_expiry, self.authorization_qas = check_token_expiry(self.token_expiry, self.authorization_qas)  # Verifica se o token expirou antes de enviar uma solicitação
        print("TEMPO PORRA: ", self.token_expiry)
        post_fileuploader = f"{self.prefix_fileuploader}"

        headers = {'vendor-id': 'fileuploader-ygg-rvv',
                   'token': f'{self.authorization_qas}',  # Não esta atribuindo o valor do TOKEN
                   'Accept': 'application/json'}
        print("AUTORIZACAO QAS: ", self.authorization_qas)

        file_name, file_content = prepare_upload_data(self.LIST_FILES)

        files = {"files": (file_name, file_content, "image/jpeg")}

        response = self.client.post(post_fileuploader, headers=headers, files=files, name="Post - File Uploader")
        print("Response: ", response)
        print("File name: ", file_name)

        handle_response(response, file_name, self.authorization_qas)
