from flask import (
    Flask, # Cria aplicação web
    render_template, # Abre as páginas HTML
    request, # Captura as informações que foram enviadas pelos formulários HTML
    redirect, # Redireciona o usuário para outra página
    url_for, # Cria URLs automaticamente usando o nome da função
    session # Guarda informações do usuário logado
)

from dotenv import load_dotenv # Biblioteca que lê o arquivo .env
import os # Biblioteca do Python que acessa variáveis do sistema
from database import Database # Importa a classe responsável pela conexão com o banco MySQL
from services import * # Importa todos os serviços do sistema

load_dotenv() # Carrega as variáveis armazenadas no arquivo .env
app = Flask(__name__) # Cria a aplicação Flask, o parâmetro __name__ informa ao Flask onde a aplicação está localizada
app.secret_key = "scsc_secret_key" # Chave secreta utilizada para proteger as sessões dos usuários, assim o Flask consegue armazenar informações na session

# ___________________________________________________________________________
# BANCO DE DADOS
db = Database(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

db.connect() # Realiza a conexão com o banco MySQL

# ___________________________________________________________________________
# TABELA USERS
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20)
)
"""

db.execute_query(create_users_table) # Executa o comando SQL

# ___________________________________________________________________________
# TABELA REQUESTS
create_requests_table = """
CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100),
    description TEXT,
    urgency INT,
    impact_level INT,
    priority VARCHAR(20),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
)
"""

db.execute_query(create_requests_table) # Executa o comando SQL

# ___________________________________________________________________________
# HOME
@app.route("/") # Define a rota da página
def home():

    return render_template(
        "home.html"
    )

# ___________________________________________________________________________
# LOGIN PAGE
@app.route("/login-page") # Define a rota da página
def login_page():

    return render_template(
        "login.html"
    )

# ___________________________________________________________________________
# LOGIN
@app.route("/login", methods=["POST"]) # Define a rota da página | POST - Método usado para enviar dados do formulário
def login():

    email = request.form["email"] # Pega os dados digitados pelo usuário no formulário HTML
    password = request.form["password"] # Pega a senha fornecida pelo usuário no formulário HTML
    result = login_user_service(
        db,
        email,
        password
    )

    # Se der certo, abre a sessão do usuário
    if result["success"]:
        session["user_id"] = result["user"]["id"]
        session["user_name"] = result["user"]["name"]

        # Direciona ele para o dashboard
        return redirect(
            url_for("dashboard")
        )

    # Se der errado, retorna mensagem de erro
    return render_template(
        "login.html",
        error=result["message"]
    )

# ___________________________________________________________________________
# CADASTRO PAGE
@app.route("/cadastro") # Define a rota da página.
def cadastro_page():

    # Direciona o usuário à página de cadastro
    return render_template(
        "cadastro.html"
    )

# ___________________________________________________________________________
# CADASTRO
@app.route("/register", methods=["POST"]) # Define a rota da página.
def register():

    # Pega os dados digitados pelo usuário no formulário HTML
    name = request.form["nome"]
    email = request.form["email"]
    phone = request.form["tel"]
    password = request.form["senha"]

    # Registra e salva os dados no banco
    result = register_user_service(
        db,
        name,
        email,
        phone,
        password
    )

    if result["success"]:

        # Cadastra o usuário no banco
        return render_template(
            "cadastro.html",
            message="Cadastro realizado com sucesso!"
        )

    # Retorna um erro ao cadastrar
    return render_template(
        "cadastro.html",
        error=result["message"]
    )

# ___________________________________________________________________________
# DASHBOARD
@app.route("/dashboard") # Define a rota da página.
def dashboard():

    if "user_id" not in session:
        return redirect(
            url_for("login_page")
        )

    # Inicia a sessão do usuário de acordo com seus dados salvos no banco
    requests = get_requests_by_user(
        db,
        session["user_id"]
    )

    # Mensagem de entrada em caso de sucesso
    success_message = session.pop(
        "success_message",
        None
    )

    return render_template(
        "dashboard.html",
        requests=requests,
        user_name=session["user_name"],
        success_message=success_message
    )

# ___________________________________________________________________________
# REDIRECIONAR OPÇÕES
@app.route("/redirecionar-opcao",methods=["POST"]) # Define a rota da página.
def redirecionar_opcao():

    # Lista as opções disponíveis
    opcao = request.form["opcao"]

    # Se o usuário escolher a opção correspondente a determinado nº, ele será levado para a página escolhida
    if opcao == "1":
        return redirect(
            url_for("criar_solicitacao_page")
        )

    elif opcao == "2": # Usuário seleciona
        return redirect(
            url_for("usuarios") # Usuário é redirecionado para página específica
        )

    elif opcao == "3":
        return redirect(
            url_for("solicitacoes")
        )

    elif opcao == "4":
        return redirect(
            url_for("listar_por_status")
        )

    elif opcao == "5":
        return redirect(
            url_for("listar_por_prioridade")
        )

    elif opcao == "6":
        return redirect(
            url_for("listar_por_usuario")
        )

    elif opcao == "7":
        return redirect(
            url_for("atualizar_status")
        )

    elif opcao == "8":
        return redirect(
            url_for("pesquisar_solicitacoes")
        )

    elif opcao == "9":
        return redirect(
            url_for("cancelar_solicitacao")
        )
    
    elif opcao == "10":
        return redirect(
            url_for("estatisticas_status")
        )
    
    elif opcao == "11":
        return redirect(
            url_for("estatisticas_prioridade")
        )

    return redirect(
        url_for("dashboard")
    )

# ___________________________________________________________________________
# CRIAR SOLICITAÇÃO
@app.route("/criar-solicitacao") # Define a rota da página.
def criar_solicitacao_page():

    # Usuário acessa a página de criar solicitação específica com seus dados (nome)
    return render_template(
        "criar_solicitacao.html",
        user_name=session["user_name"]
    )

# ___________________________________________________________________________
# SALVAR SOLICITAÇÃO
@app.route("/salvar-solicitacao", methods=["POST"]) # Define a rota da página.
def salvar_solicitacao():

    # Pega os dados fornecidos pelo usuário
    category = request.form["categoria"]
    description = request.form["descricao"]
    urgency = int(request.form["urgencia"])
    impact = int(request.form["impacto"])

    # Cria uma solicitação utilizando o id do usuário e os dados
    create_request_service(
        db,
        session["user_id"],
        category,
        description,
        urgency,
        impact
    )

    # Retorna mensagem de sucesso
    return render_template(
        "criar_solicitacao.html",
        message="Solicitação cadastrada com sucesso!"
    )

# ___________________________________________________________________________
# LISTAR USUÁRIOS
@app.route("/usuarios") # Define a rota da página.
def usuarios():

    # Pega a lista dos usuários existentes no banco
    users = list_users_service(db)

    # Retorna os dados dos usuários
    return render_template(
        "listar_usuario.html",
        users=users
    )

# ___________________________________________________________________________
# TODAS SOLICITAÇÕES
@app.route("/solicitacoes") # Define a rota da página.
def solicitacoes():

    # Pega as solicitações existentes no banco
    requests = list_all_requests_service(db)

    # Retorna as solicitações
    return render_template(
        "listar_solicitacoes.html",
        requests=requests
    )

# ___________________________________________________________________________
# LISTAR POR STATUS
@app.route("/listar-por-status") # Define a rota da página.
def listar_por_status():

    # Pega as solicitações de acordo com seus status no banco de dados
    requests = list_requests_by_status_service(db)

    # Essas são as opções de status
    abertas = []
    andamento = []
    finalizadas = []
    canceladas = []

    # Se o status da solicitação estiver como:
    for request in requests:

        # Retorna "Em aberto"
        if request[5] == "Em aberto":
            abertas.append(request)

        # Retorna "Em andamento"
        elif request[5] == "Em andamento":
            andamento.append(request)

        # Retorna "Finalizada"
        elif request[5] == "Finalizada":
            finalizadas.append(request)

        # Retorna "Cancelada"
        elif request[5] == "Cancelada":
            canceladas.append(request)

    # Retorna todas as solicitações separadas por seus respectivos status
    return render_template(
        "listar_status.html",
        abertas=abertas,
        andamento=andamento,
        finalizadas=finalizadas,
        canceladas=canceladas
    )

# ___________________________________________________________________________
# LISTAR POR PRIORIDADE
@app.route("/listar-por-prioridade") # Define a rota da página.
def listar_por_prioridade():

    # Pega as solicitações de acordo com sua prioridade no banco de dados
    requests = list_requests_by_priority_service(db)

    # Essas são as opções de prioridade
    altas = []
    medias = []
    baixas = []

     # Se a prioridade da solicitação estiver como:
    for request in requests:
        print("PRIORIDADE:", request[4])

        # Retorna "Alta"
        if request[4] == "Alta":
            altas.append(request)
        
        # Retorna "Média"
        elif request[4] == "Média":
            medias.append(request)

        # Retorna "Baixa"
        elif request[4] == "Baixa":
            baixas.append(request)

    # Retorna todas as solicitações separadas por seus respectivos status
    return render_template(
        "listar_prioridades.html",
        altas=altas,
        medias=medias,
        baixas=baixas
    )

# ___________________________________________________________________________
# LISTAR POR USUÁRIO
@app.route("/listar-por-usuario") # Define a rota da página.
def listar_por_usuario():

    # Pega as solicitações separadas por usuário
    requests = list_requests_by_user_service(db)
    usuarios = {}

    # Para cada uma existem um usuário correposdente
    for request in requests:
        nome_usuario = request[1]
        if nome_usuario not in usuarios:
            usuarios[nome_usuario] = []
        usuarios[nome_usuario].append(request)

    # Retorna as solicitações de acordo com quem a criou
    return render_template(
        "listar_por_usuario.html",
        usuarios=usuarios
    )

# ___________________________________________________________________________
# ATUALIZAR STATUS
@app.route("/atualizar-status", methods=["GET", "POST"]) # Define a rota da página.
def atualizar_status():
    message = None # Nenuma mensagem inicial

    # Se o método for POST
    if request.method == "POST":
        request_id = request.form["request_id"] # Pega o id da solicitação
        new_status = request.form["new_status"] # Fornece a opção de atualizar o status

        # Atualiza o status, mantendo o id da solicitação
        result = update_request_status_service(
            db,
            request_id,
            new_status
        )
        # Mensagem de sucesso se der certo
        message = result["message"] if not result["success"] else "Status atualizado com sucesso!"

    return render_template(
        "atualizar_status.html",
        message=message
    )

# ___________________________________________________________________________
# ESTATÍSTICAS
# POR STATUS
@app.route("/estatisticas-status") # Define a rota da página
def estatisticas_status():

    # Estatísticas por status
    stats = stats_by_status_service(db)

    # Retorna a quantidade de solicitações por status
    return render_template(
        "estatisticas_status.html",
        stats=stats
    )

# POR PRIORIDADE
@app.route("/estatisticas-prioridade") # Define a rota da página
def estatisticas_prioridade():

    # Estatísticas por status
    stats = stats_by_priority_service(db)

    # Retorna a quantidade de solicitações por status
    return render_template(
        "estatisticas_prioridade.html",
        stats=stats
    )

# ___________________________________________________________________________
# LOGOUT
@app.route("/logout") # Define a rota da página
def logout():

    # Limpa a sessão, removendo todos os dados ou chaves armazenados em uma sessão ativa
    session.clear() # deixa ela vazia

    # Leva o usuário para a página home
    return redirect(
        url_for("home")
    )

# ___________________________________________________________________________
# CANCELAR SOLICITAÇÃO
@app.route("/cancelar-solicitacao",methods=["GET", "POST"]) # Define a rota da página
def cancelar_solicitacao():
    message = None

    if request.method == "POST":
        request_id = request.form["request_id"]
        result = cancel_request_service(
            db,
            request_id
        )
        message = result["message"]

    return render_template(
        "cancelar_solicitacao.html",
        message=message
    )

# ___________________________________________________________________________
# PESQUISAR SOLICITAÇÕES
@app.route("/pesquisar-solicitacoes",methods=["GET", "POST"]) # Define a rota da página
def pesquisar_solicitacoes():
    
    requests = [] # Pega as solicitações
    mensagem = None # Nenhuma mensagem

    # Se estiver no método POST
    if request.method == "POST":

        termo = request.form["termo"] # Pega o termo escrito pelo usuário

        # Procura o termo dentro do banco de dados
        requests = search_requests_service(
            db,
            termo
        )

        # Se não existir, retorna mensagem de erro
        if not requests:
            mensagem = "Nenhuma solicitação encontrada! Tente novamente"

    # Se existir, retorna a(s) solicitação(ções) encontrada(s)
    return render_template(
        "pesquisar_solicitacoes.html",
        requests=requests,
        mensagem=mensagem
    )

# ___________________________________________________________________________
# FLASK
if __name__ == "__main__": # Garante que o servidor será ligado somente se executar o arquivo diretamente pelo terminal 
    # (ex: python app.py)

    app.run(debug=True) # Inicia o servidor local integrado. 