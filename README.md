# Performance Tests - File Uploader

## Descrição

Este projeto realiza testes de desempenho para upload de arquivos utilizando a biblioteca Locust. O teste consiste em enviar várias imagens para um servidor e verificar o tempo de resposta e o comportamento do servidor sob carga.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- `locustfile.py`: Arquivo principal que define a classe de usuário do Locust e as tarefas de teste.
- `auth.py`: Módulo responsável por gerenciar a autenticação, incluindo a obtenção e renovação do token.
- `rules.py`: Módulo que define regras e manipulação de dados, como preparação dos dados de upload e tratamento das respostas do servidor.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone <https://github.com/emersinrp/brf_performance_fileuploader.git>
   cd <brf_performance_fileuploader>
   
2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash 
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

4. **Configure as variáveis de ambiente:**
Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:
   ```bash
   KONG_FILEUPLOADER_QAS=<URL_DO_SERVIDOR>
   PREFIX_FILEUPLOADER=<PREFIXO_DA_URL_DE_UPLOAD>

## Utilização do Locust

1. **Executando os testes:**
Para executar os testes de performance, utilize o comando abaixo no terminal:
   ```bash
   locust -f locustfiles/locustfile.py --class-picker : Esta execução permite escolher uma classe específica de usuário para executar os testes. O argumento --class-picker permite selecionar a classe de usuário a ser utilizada a partir do arquivo especificado com -f. Isso é útil quando há várias classes de usuário definidas no arquivo e deseja-se executar apenas uma delas.  
   locust -f locustfile.py :  Nesta execução, o Locust será iniciado com o arquivo locustfile.py fornecido com a definição das classes de usuário e tarefas. O Locust iniciará com os valores padrão de usuários virtuais e taxa de geração de usuários.
   locust --headless -f locustfiles/locustfile.py --users 1 --spawn-rate 1 : Esta execução inicia o Locust em modo "headless", ou seja, sem a interface gráfica. O arquivo locustfile.py é especificado com -f, e apenas um usuário virtual será criado com uma taxa de geração de um usuário por segundo.
   locust --headless -f locustfiles/locustfile.py --tags test1 --users 1 --spawn-rate 1 : Similar à execução anterior, mas este comando adiciona a opção --tags test1, que executa apenas as tarefas marcadas com a tag "test1". Isso é útil para executar apenas um conjunto específico de tarefas definidas no arquivo locustfile.py 

3. **Bibliotecas Utilizadas**
   ```bash
   Locust: Ferramenta de carga de código aberto em Python para simular usuários simultâneos.  
   python-dotenv: Utilizada para carregar variáveis de ambiente a partir de um arquivo .env.  
   requests: Biblioteca para realizar requisições HTTP de forma simples.

3. **Estrutura do Código**:

**locustfile.py:**  
Define a classe PostFileUploader que herda de HttpUser do Locust. Inclui a tarefa post_file_uploader que realiza o upload de arquivos para o servidor.  

**auth.py:**  
Contém funções para gerenciar tokens de autenticação:
refresh_token(): Obtém um novo token.  
check_token_expiry(): Verifica se o token expirou e renova se necessário.  
get_authentication(): Gera o token inicial.  

**rules.py:**  
Define funções auxiliares:  
prepare_upload_data(file_list): Prepara o arquivo para upload escolhendo aleatoriamente um arquivo da lista.  
handle_response(response, file_name, authorization_qas): Manipula a resposta do servidor após o upload.  

## Como Contribuir
   ```bash
    Faça um fork do projeto.  
    Crie uma nova branch: git checkout -b minha-feature.  
    Faça suas alterações e adicione commits: git commit -m 'Minha nova feature'.  
    Envie para a branch original: git push origin minha-feature.  
    Crie um pull request.  