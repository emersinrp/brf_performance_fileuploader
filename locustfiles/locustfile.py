import random
from locust import HttpUser, task, between
import os
from dotenv import load_dotenv
from helpers.auth import refresh_tokens, check_token_expiry
from helpers.rules import prepare_upload_data, handle_response

load_dotenv()


class PostFileUploader(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_token_expiry = None
        self.auth_token = None
        self.new_token_expiry = None
        self.new_token = None

    host = os.environ["KONG_FILEUPLOADER_QAS"]
    wait_time = between(2, 5)
    prefix_fileuploader = os.environ["PREFIX_FILEUPLOADER"]
    LIST_FILES = ["imagens_teste/teste_img_1.jpg",
                  "imagens_teste/teste_img_5.jpg",
                  "imagens_teste/teste_img_6.jpg",
                  "imagens_teste/teste_img_9.jpg",
                  "imagens_teste/teste_img_10.jpg",
                  "imagens_teste/teste_img_12.jpg",
                  "imagens_teste/teste_img_14.jpg"]

    def on_start(self):
        self.auth_token, self.auth_token_expiry, self.new_token, self.new_token_expiry = refresh_tokens()
        # Obtém os tokens iniciais

    @task
    def post_file_uploader(self):
        self.auth_token_expiry, self.auth_token, self.new_token_expiry, self.new_token = check_token_expiry(
            self.auth_token_expiry, self.auth_token, self.new_token_expiry, self.new_token)
        post_fileuploader = f"{self.prefix_fileuploader}"
        headers = {
            'vendor-id': 'fileuploader-ygg-rvv',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.new_token}',  # Atualiza o valor do novo token Ygg
            'token': self.auth_token  # Adiciona o token de autenticação File Uploader
        }

        num_files = random.randint(1, len(self.LIST_FILES))
        # Número aleatório de arquivos entre 1 e o total de arquivos disponíveis
        files = prepare_upload_data(self.LIST_FILES, num_files)
        files_data = [("files", (file_name, content, "image/jpeg")) for file_name, content in files.items()]

        response = self.client.post(post_fileuploader, headers=headers, files=files_data, name="Post - File Uploader")

        handle_response(response, list(files.keys()), self.new_token)