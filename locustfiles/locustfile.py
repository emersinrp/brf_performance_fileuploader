import random
import time
from locust import HttpUser, task, between, tag
import os
from dotenv import load_dotenv
from helpers.auth import refresh_token, check_token_expiry, authorization_qas, get_authentication
from helpers.rules import prepare_upload_data, handle_response

load_dotenv()


class PostFileUploader(HttpUser):
    host = os.environ["KONG_FILEUPLOADER_QAS"]
    wait_time = between(1.0, 3.0)
    prefix_fileuploader = os.environ["PREFIX_FILEUPLOADER"]
    LIST_FILES = ["imagens_teste/teste_img_2.jpg"]

    def on_start(self):
        refresh_token()  # Chamando o método para obter o token inicial
        global token_expiry
        token_expiry = time.time() + 1800  # Definindo o tempo de validade do token para 30 minutos à frente

    @task
    def post_file_uploader(self):
        check_token_expiry()  # Verifica se o token expirou antes de enviar uma solicitação
        post_fileuploader = f"{self.prefix_fileuploader}"

        headers = {'vendor-id': 'fileuploader-ygg-rvv',
                   'token': f'{authorization_qas}', # Não esta atribuindo o valor do TOKEN
                   'Accept': 'application/json'}
        print("AUTORIZACAO QAS: ", authorization_qas)

        file_name, file_content = prepare_upload_data(self.LIST_FILES)

        files = {"files": (file_name, file_content, "image/jpeg")}

        response = self.client.post(post_fileuploader, headers=headers, files=files, name="Post - File Uploader")
        print("Response: ", response)
        print("File name: ", file_name)

        handle_response(response, file_name, authorization_qas)
