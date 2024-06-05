import random
from helpers.auth import refresh_tokens


def prepare_upload_data(file_list, num_files):
    selected_files = random.sample(file_list, k=num_files)  # Seleciona aleatoriamente 'num_files' arquivos
    files = {}
    for file_name in selected_files:
        with open(file_name, "rb") as file:
            files[file_name] = file.read()
    return files


def handle_response(response, file_names, authorization_qas):  # Regras para execucao do POST
    if response.status_code == 200:
        resposta = response.json()
        if resposta['container'] == "teste2":
            print(f"==== Envio realizado com sucesso ====\n"
                  f"Stored file names: {[file['stored_file_name'] for file in resposta['files']]} \n",
                  f"File names: {[file['real_file_name'] for file in resposta['files']]} \n",
                  f"Urls: {[file['url'] for file in resposta['files']]} \n"
                  f"Imagens enviadas: {file_names} \n")
        else:
            print(f"==== Erro ao enviar POST ==== \n"
                  f"{response.text}, {response.status_code} "
                  f"Imagens enviadas: {file_names} \n")
    elif response.status_code == 401:
        print("Refresh token response: 401")
        return refresh_tokens()
    else:
        print(f"==== FALHA NA REQUISIÇÃO ====\n"
              f"Status Code: {response.status_code}\n"
              f"Response Text: {response.text}\n"
              f"Headers: {response.headers}\n"
              f"Request Headers: {response.request.headers}\n"
              f"Imagens enviadas: {file_names} \n")
