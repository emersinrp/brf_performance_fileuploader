import random
from helpers.auth import refresh_token


def prepare_upload_data(file_list):  # prepare the file for upload
    file_name = random.choice(file_list)
    with open(file_name, "rb") as file:
        file_content = file.read()
    return file_name, file_content


def handle_response(response, file_name, authorization_qas):  # rules for executing the post
    if response.status_code == 200:
        resposta = response.json()
        if resposta['container'] == "teste2":
            print(f"==== Envio realizado com sucesso ====\n"
                  f"Stored file name: {resposta['files'][0]['stored_file_name']} \n",
                  f"File name: {resposta['files'][0]['real_file_name']} \n",
                  f"Url: {resposta['files'][0]['url']} \n"
                  f"Imagem enviada: {file_name} \n")
        else:
            print(f"==== Erro ao enviar POST ==== \n"
                  f" {response.text}, {response.status_code} "
                  f"Imagem enviada: {file_name} \n")
    elif response.status_code == 401:
        print("Refresh token response: 401")
        return refresh_token()
    else:
        print("==== FALHA NA REQUISIÇÃO ====")
