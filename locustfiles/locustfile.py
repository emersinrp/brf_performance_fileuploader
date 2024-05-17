from locust import HttpUser, task, between, tag
import os
from dotenv import load_dotenv
from helpers.auth import refresh_token, check_token_expiry
from helpers.rules import prepare_upload_data, handle_response

load_dotenv()


class PostFileUploader(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_expiry = None
        self.authorization_qas = None

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
        self.authorization_qas, self.token_expiry = refresh_token()  # calling the method to get the initial token

    @task
    def post_file_uploader(self):
        self.token_expiry, self.authorization_qas = check_token_expiry(self.token_expiry,
                                                                       self.authorization_qas)  # checks whether the
        # token has expired before sending a request
        post_fileuploader = f"{self.prefix_fileuploader}"
        headers = {
            'vendor-id': 'fileuploader-ygg-rvv',
            'token': f'{self.authorization_qas}',  # updating the token value
            'Accept': 'application/json'
        }

        file_name, file_content = prepare_upload_data(self.LIST_FILES)
        files = {"files": (file_name, file_content, "image/jpeg")}

        response = self.client.post(post_fileuploader, headers=headers, files=files, name="Post - File Uploader")

        handle_response(response, file_name, self.authorization_qas)
