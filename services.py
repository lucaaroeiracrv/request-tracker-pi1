# services.py - contains the main business logic for the request tracking system, including user registration, login, request creation, and listing requests based on various criteria.
from auth import hash_password, check_password, is_valid_email, is_valid_password
import pwinput

# predefined list of available request categories
CATEGORY_OPTIONS = ["TI", "RH", "Financeiro", "Infraestrutura", "Suporte"]

def register_user(db):# handles user registration
    # collect user input
    name = input("Nome: ").strip()
    email = input("Email: ").strip()
    phone = input("Telefone (opcional): ").strip()
    password = pwinput.pwinput(prompt="Senha (mín. 6 caracteres): ").strip()

    # validate required fields
    if not name:
        print("Nome é obrigatório.")
        return
    if not email and not phone:
        print("Informe pelo menos um meio de contato (email ou telefone).")
        return
    if email and not is_valid_email(email):
        print("Email inválido.")
        return
    if not is_valid_password(password):
        print("Senha muito curta.")
        return

    # hash the password before storing it
    password_hash = hash_password(password) 

    # SQL query to insert a new user
    query = """
        INSERT INTO users (name, email, phone, password_hash)
        VALUES (%s, %s, %s, %s)
    """
    try: # execute insert with safe parameter binding
        db.execute_query(query, (name, email if email else None, phone if phone else None, password_hash))
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        if "1062" in str(e) or "UNIQUE" in str(e).upper(): # handle duplicate email constraint
            print("Erro ao cadastrar usuário: email já cadastrado.")
        else:
            print(f"Erro ao cadastrar usuário: {e}")

# authenticates a user using email and password
def login_user(db):
    email = input("Email: ").strip()
    password = pwinput.pwinput(prompt="Senha: ").strip()

    query = "SELECT id, name, password_hash FROM users WHERE email = %s" # retrieve user credentials by email
    result = db.execute_query(query, (email,))

    if not result: # check if user exist
        print("Usuário não encontrado.")
        return None
    user_id, name, password_hash = result[0] # unpack the result to get user id, name, and password hash

    if check_password(password, password_hash): # compare provided password with stored hash
        print(f"Login OK! Bem-vindo, {name}")
        return {"id": user_id, "name": name, "email": email}
    else:
        print("Senha incorreta.")
        return None


def list_users(db): # lists all registered users
    query = "SELECT id, name, email, phone FROM users ORDER BY name"
    users = db.execute_query(query)

    if not users:
        print("Nenhum usuário cadastrado.")
        return []

    print("\nUsuários cadastrados:")
    print("ID | Nome | Email | Telefone")
    for u in users:
        print(f"{u[0]} | {u[1]} | {u[2] or '-'} | {u[3] or '-'}")

    return users


def select_user(db): # allows selection of a user from the list
    users = list_users(db)
    if not users:
        return None
 
    try: # validate user ID input
        user_id = int(input("Digite o ID do usuário responsável pela solicitação: ").strip())
    except ValueError:
        print("ID inválido.")
        return None

    for u in users: # search for the selected user
        if u[0] == user_id:
            return u

    print("Usuário não encontrado.")
    return None


def calculate_priority(urgency, impact): # calculates request priority based on urgency and impact
    total = urgency + impact
    if total <= 3:
        return "Baixa"
    elif total <= 7:
        return "Media"
    else:
        return "Alta"


def create_request(db): # creates a new request
    user = select_user(db) # select the user related to the request
    if not user:
        return

    print("\nCategorias disponíveis:") # display available categories
    for i, c in enumerate(CATEGORY_OPTIONS, start=1):
        print(f"{i} - {c}")

    try:   # validate category selection
        category_choice = int(input("Escolha categoria: ").strip())
        category = CATEGORY_OPTIONS[category_choice - 1]
    except (ValueError, IndexError):
        print("Categoria inválida.")
        return
    
    # validate description
    description = input("Descrição da solicitação (obrigatório): ").strip()
    if not description:
        print("Descrição é obrigatória.")
        return

    try: # collect urgency and impact values
        urgency = int(input("Urgência (1 a 5): ").strip())
        impact = int(input("Impacto (1 a 5): ").strip())
    except ValueError:
        print("Urgência e impacto devem ser números inteiros.")
        return

    if not (1 <= urgency <= 5 and 1 <= impact <= 5): # validate urgency and impact ranges
        print("Urgência e impacto devem estar entre 1 e 5.")
        return
    
    # calculate derived fields
    priority = calculate_priority(urgency, impact)
    status = "Aberta"

    # insert the request into the database
    query = """
        INSERT INTO requests (user_id, category, description, urgency, impact, priority, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        db.execute_query(query, (user[0], category, description, urgency, impact, priority, status))
        print(f"Solicitação criada com sucesso! Prioridade: {priority}")
    except Exception as e:
        print(f"Erro ao criar solicitação: {e}")

def get_requests(db, where_clause=None, params=None): # retrieves requests with an optional filter condition
    query = """
        SELECT r.id, u.name, r.category, r.description, r.priority, r.status, r.created_at
        FROM requests r
        JOIN users u ON r.user_id = u.id
    """
    if where_clause:
        query += " WHERE " + where_clause

    query += " ORDER BY r.created_at DESC"
    return db.execute_query(query, params or ())

def list_requests(db): # lists all requests
    requests = get_requests(db)
    if not requests:
        print("Nenhuma solicitação encontrada.")
        return

    print("\nSolicitações:")
    print(f"{'ID':<5} | {'Solicitante':<20} | {'Categoria':<15} | {'Prioridade':<12} | {'Status':<12} | {'Data':<15}\n")
    for r in requests:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[4]:<12} | {r[5]:<12} | {r[6]}")


def list_requests_by_status(db): # lists requests filtered by status
    status = input("Status (Aberta/Em andamento/Fechada): ").strip().title()
    if status not in ["Aberta", "Em andamento", "Fechada"]:
        print("Status inválido.")
        return

    requests = get_requests(db, "r.status = %s", (status,))
    if not requests:
        print(f"Nenhuma solicitação com status {status}.")
        return

    print(f"\nSolicitações com status {status}:")
    print(f"{'ID':<5} | {'Solicitante':<20} | {'Categoria':<15} | {'Prioridade':<12} | {'Status':<12} | {'Data':<15}\n")
    for r in requests:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[4]:<12} | {r[5]:<12} | {r[6]}")


def list_requests_by_priority(db): # lists requests filtered by priority
    priority = input("Prioridade (Baixa/Média/Alta): ").strip().title()
    if priority not in ["Baixa", "Media", "Alta"]:
        print("Prioridade inválida.")
        return

    requests = get_requests(db, "r.priority = %s", (priority,))
    if not requests:
        print(f"Nenhuma solicitação com prioridade {priority}.")
        return

    print(f"\nSolicitações com prioridade {priority}:")
    print(f"{'ID':<5} | {'Solicitante':<20} | {'Categoria':<15} | {'Prioridade':<12} | {'Status':<12} | {'Data':<15}\n")
    for r in requests:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[4]:<12} | {r[5]:<12} | {r[6]}")


def list_requests_by_user(db): # lists requests created by a specific user
    user = select_user(db)
    if not user:
        return

    requests = get_requests(db, "r.user_id = %s", (user[0],))
    if not requests:
        print(f"Nenhuma solicitação para o usuário {user[1]}.")
        return

    print(f"\nSolicitações do usuário {user[1]}:")
    print(f"{'ID':<5} | {'Solicitante':<20} | {'Categoria':<15} | {'Prioridade':<12} | {'Status':<12} | {'Data':<15}\n")
    for r in requests:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[4]:<12} | {r[5]:<12} | {r[6]}")


def update_request_status(db): # updates the status of an existing request
    try:
        request_id = int(input("ID da solicitação: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    # retrieve current status
    result = db.execute_query("SELECT status FROM requests WHERE id = %s", (request_id,))
    if not result:
        print("Solicitação não encontrada.")
        return

    current = result[0][0]
    print(f"Status atual: {current}")

    if current == "Fechada": # prevent reopening closed requests
        print("Não é possível reabrir solicitação fechada.")
        return

    # validate new status input
    status = input("Novo status (Em andamento/Fechada): ").strip().title()
    if status not in ["Em andamento", "Fechada"]:
        print("Status inválido.")
        return

    if current == "Aberta" and status == "Fechada": # prevent invalid status transitions
        pass
    if current == "Em andamento" and status == "Aberta":
        print("Transição inválida: não pode voltar de Em andamento para Aberta.")
        return

    # update status and timestamp
    db.execute_query("UPDATE requests SET status = %s, updated_at = NOW() WHERE id = %s", (status, request_id))
    print("Status atualizado com sucesso.")


def stats_by_status(db): # displays statistics grouped by request status
    query = "SELECT status, COUNT(*) FROM requests GROUP BY status"
    rows = db.execute_query(query)
    if not rows:
        print("Nenhuma solicitação cadastrada.")
        return

    print("\nEstatísticas por status:")
    for s, c in rows:
        print(f"{s}: {c}")


def stats_by_priority(db): # displays statistics grouped by request priority
    query = "SELECT priority, COUNT(*) FROM requests GROUP BY priority"
    rows = db.execute_query(query)
    if not rows:
        print("Nenhuma solicitação cadastrada.")
        return

    print("\nEstatísticas por prioridade:")
    for p, c in rows:
        print(f"{p}: {c}")
