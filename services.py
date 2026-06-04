'''
# services.py - contains the main business logic for the request tracking system, including user registration,
# login, request creation, and listing requests based on various criteria.

from auth import hash_password, check_password, is_valid_email, is_valid_password
import pwinput

# Predefined list of available request categories
CATEGORY_OPTIONS = ["TI", "RH", "Financeiro", "Infraestrutura", "Suporte"]

STATUS_OPTIONS = ["Aberta", "Em andamento", "Fechada", "Cancelada"]
PRIORITY_OPTIONS = ["Baixa", "Media", "Alta"]  # manter compatível com o banco atual

'''
'''
# ========= Formatting helpers (tables) =========
def _truncate(text: object, max_len: int) -> str:
    text = "" if text is None else str(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _print_table(title: str, columns: list[tuple[str, int]], rows: list[list[object]]) -> None:
    """
    columns: [(header, width), ...]
    rows: list of rows, each row is list of values aligned to columns
    """
    header = "  ".join(f"{name:<{width}}" for name, width in columns)
    line = "-" * len(header)

    print(f"\n{title}")
    print(line)
    print(header)
    print(line)

    for row in rows:
        formatted = []
        for (col_name, width), value in zip(columns, row):
            formatted.append(f"{_truncate(value, width):<{width}}")
        print("  ".join(formatted))

    print(line)
'''
'''
# ========= Input/validation helpers =========
def ask_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Campo obrigatório. Tente novamente.")


def ask_int(prompt: str, *, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Valor inválido: digite um número inteiro.")
            continue

        if min_value is not None and value < min_value:
            print(f"Valor inválido: deve ser >= {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Valor inválido: deve ser <= {max_value}.")
            continue
        return value


def ask_choice(prompt: str, options: list[str]) -> str:
    """Mostra opções numeradas e devolve o item escolhido (obrigatório escolher)."""
    print()
    for i, opt in enumerate(options, start=1):
        print(f"[{i}] {opt}")

    choice = ask_int(prompt, min_value=1, max_value=len(options))
    return options[choice - 1]


def ask_email(prompt: str = "Email: ") -> str:
    while True:
        email = ask_non_empty(prompt)
        if is_valid_email(email):
            return email
        print("Email inválido. Tente novamente.")


def ask_password(prompt: str, *, min_len: int = 6) -> str:
    while True:
        password = pwinput.pwinput(prompt=prompt).strip()
        if not password:
            print("Senha é obrigatória.")
            continue
        if is_valid_password(password) and len(password) >= min_len:
            return password
        print(f"Senha inválida. Mínimo recomendado: {min_len} caracteres.")
'''
'''
def ask_phone_optional(prompt: str = "Telefone (opcional): ", *, min_len: int = 8) -> str | None:
    """
    Telefone é opcional:
    - vazio => None
    - preenchido => precisa ter pelo menos min_len caracteres (apenas isso)
    """
    while True:
        phone = input(prompt).strip()
        if not phone:
            return None
        if len(phone) >= min_len:
            return phone
        print(f"Telefone inválido: precisa ter pelo menos {min_len} caracteres (ou deixe em branco).")


def calculate_priority(urgency: int, impact: int) -> str:
    total = urgency + impact
    if total <= 3:
        return "Baixa"
    elif total <= 7:
        return "Media"
    else:
        return "Alta"


# ========= Users =========
def register_user(db):
    name = ask_non_empty("Nome: ")
    email = ask_email("Email: ")
    phone = ask_phone_optional("Telefone (opcional): ", min_len=8)
    password = ask_password("Senha (mín. 6 caracteres): ", min_len=6)

    password_hash = hash_password(password)

    query = """
        INSERT INTO users (name, email, phone, password_hash)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute_query(query, (name, email, phone, password_hash))
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        # MySQL duplicate key costuma ser 1062
        if "1062" in str(e) or "UNIQUE" in str(e).upper():
            print("Erro ao cadastrar usuário: email já cadastrado.")
        else:
            print(f"Erro ao cadastrar usuário: {e}")
'''
'''
def login_user(db):
    email = ask_email("Email: ")
    password = pwinput.pwinput(prompt="Senha: ").strip()
    if not password:
        print("Senha é obrigatória.")
        return None

    query = "SELECT id, name, password_hash FROM users WHERE email = %s"
    result = db.execute_query(query, (email,))

    if not result:
        print("Usuário não encontrado.")
        return None

    user_id, name, password_hash = result[0]

    if check_password(password, password_hash):
        print(f"Login OK! Bem-vindo, {name}")
        return {"id": user_id, "name": name, "email": email}

    print("Senha incorreta.")
    return None


def list_users(db):
    query = "SELECT id, name, email, phone FROM users ORDER BY name"
    users = db.execute_query(query)

    if not users:
        print("Nenhum usuário cadastrado.")
        return []

    columns = [
        ("ID", 4),
        ("Nome", 22),
        ("Email", 28),
        ("Telefone", 16),
    ]
    rows = []
    for user_id, name, email, phone in users:
        rows.append([user_id, name, email, phone or "-"])

    _print_table("Usuários cadastrados:", columns, rows)
    return users
'''
'''
def select_user(db):
    users = list_users(db)
    if not users:
        return None

    valid_ids = {u[0] for u in users}

    while True:
        user_id = ask_int("Digite o ID do usuário responsável pela solicitação: ", min_value=1)
        if user_id in valid_ids:
            for u in users:
                if u[0] == user_id:
                    return u
        print("Usuário não encontrado. Tente novamente.")


# ========= Requests =========
def create_request(db):
    user = select_user(db)
    if not user:
        return

    category = ask_choice("Escolha categoria: ", CATEGORY_OPTIONS)
    description = ask_non_empty("Descrição da solicitação: ")

    urgency = ask_int("Urgência (1 a 5): ", min_value=1, max_value=5)
    impact = ask_int("Impacto (1 a 5): ", min_value=1, max_value=5)

    priority = calculate_priority(urgency, impact)
    status = "Aberta"

    query = """
        INSERT INTO requests (user_id, category, description, urgency, impact, priority, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        db.execute_query(query, (user[0], category, description, urgency, impact, priority, status))
        print(f"Solicitação criada com sucesso! Prioridade: {priority}")
    except Exception as e:
        print(f"Erro ao criar solicitação: {e}")


def get_requests(db, where_clause=None, params=None):
    query = """
        SELECT r.id, u.name, r.category, r.description, r.priority, r.status, r.created_at
        FROM requests r
        JOIN users u ON r.user_id = u.id
    """
    if where_clause:
        query += " WHERE " + where_clause

    query += " ORDER BY r.created_at DESC"
    return db.execute_query(query, params or ())


def _print_requests(title: str, rows: list[tuple]):
    if not rows:
        print("Nenhuma solicitação encontrada.")
        return

    columns = [
        ("ID", 4),
        ("Solicitante", 18),
        ("Categoria", 16),
        ("Descrição", 40),
        ("Prioridade", 10),
        ("Status", 13),
        ("Data", 19),
    ]

    table_rows = []
    for request_id, user_name, category, description, priority, status, created_at in rows:
        table_rows.append([request_id, user_name, category, description, priority, status, created_at])

    _print_table(title, columns, table_rows)


def list_requests(db):
    rows = get_requests(db)
    _print_requests("Solicitações (todas):", rows)
'''
'''
def list_requests_by_status(db):
    status = ask_choice("Escolha o status: ", STATUS_OPTIONS)

    rows = get_requests(db, "r.status = %s", (status,))
    if not rows:
        print(f"Nenhuma solicitação com status {status}.")
        return

    _print_requests(f"Solicitações com status {status}:", rows)


def list_requests_by_priority(db):
    priority = ask_choice("Escolha a prioridade: ", PRIORITY_OPTIONS)

    rows = get_requests(db, "r.priority = %s", (priority,))
    if not rows:
        print(f"Nenhuma solicitação com prioridade {priority}.")
        return

    _print_requests(f"Solicitações com prioridade {priority}:", rows)


def list_requests_by_user(db):
    user = select_user(db)
    rows = get_requests(db, "r.user_id = %s", (user[0],))
    if not rows:
        print(f"Nenhuma solicitação para o usuário {user[1]}.")
        return

    _print_requests(f"Solicitações do usuário {user[1]}:", rows)


def update_request_status(db):
    # Mostra todas as solicitações com seus IDs para o usuário escolher
    all_requests = get_requests(db)
    if not all_requests:
        print("Nenhuma solicitação cadastrada.")
        return

    _print_requests("Solicitações cadastradas (use o ID para atualizar):", all_requests)

    valid_ids = {r[0] for r in all_requests}

    while True:
        request_id = ask_int("Digite o ID da solicitação que deseja atualizar: ", min_value=1)
        if request_id in valid_ids:
            break
        print("ID inválido. Escolha um ID da lista acima.")

    # Recupera status atual
    result = db.execute_query("SELECT status FROM requests WHERE id = %s", (request_id,))
    if not result:
        print("Solicitação não encontrada.")
        return

    current = result[0][0]
    print(f"Status atual: {current}")

    # Agora permite reabrir: qualquer estado pode ir para qualquer outro (exceto manter igual)
    allowed = [s for s in STATUS_OPTIONS if s != current]
    if not allowed:
        print("Nenhuma transição disponível.")
        return

    new_status = ask_choice("Novo status: ", allowed)

    db.execute_query(
        "UPDATE requests SET status = %s, updated_at = NOW() WHERE id = %s",
        (new_status, request_id),
    )
    print("Status atualizado com sucesso.")
'''
'''
# ========= Stats =========
def stats_by_status(db):
    query = "SELECT status, COUNT(*) FROM requests GROUP BY status"
    rows = db.execute_query(query)
    if not rows:
        print("Nenhuma solicitação cadastrada.")
        return

    print("\nEstatísticas por status:")
    for s, c in rows:
        print(f"{s}: {c}")


def stats_by_priority(db):
    query = "SELECT priority, COUNT(*) FROM requests GROUP BY priority"
    rows = db.execute_query(query)
    if not rows:
        print("Nenhuma solicitação cadastrada.")
        return

    print("\nEstatísticas por prioridade:")
    for p, c in rows:
        print(f"{p}: {c}")

def cancelar_solicitacao(db):
    rows = get_requests(db)

    if not rows:
        print("Nenhuma solicitação cadastrada.")
        return

    _print_requests(
        "Solicitações cadastradas (use o ID para cancelar):",
        rows
    )

    valid_ids = {r[0] for r in rows}

    while True:
        request_id = ask_int(
            "Digite o ID da solicitação que deseja cancelar: ",
            min_value=1
        )

        if request_id in valid_ids:
            break

        print("ID inválido. Escolha um ID da lista acima.")

    result = db.execute_query(
        "SELECT status FROM requests WHERE id = %s",
        (request_id,)
    )

    if not result:
        print("Solicitação não encontrada.")
        return

    current_status = result[0][0]

    if current_status != "Aberta":
        print(
            f"Não é possível cancelar uma solicitação com status "
            f"'{current_status}'. Apenas solicitações abertas podem ser canceladas."
        )
        return

    try:
        db.execute_query(
            """
            UPDATE requests
            SET status = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            ("Cancelada", request_id)
        )

        print("Solicitação cancelada com sucesso.")

    except Exception as e:
        print(f"Erro ao cancelar solicitação: {e}")
'''
        
from auth import *

# CADASTRO
def register_user_service(
    db,
    name,
    email,
    phone,
    password
):

    if not is_valid_email(email):
        return {
            "success": False,
            "message": "Email inválido"
        }
    if not is_valid_password(password):
        return {
            "success": False,
            "message": "Senha muito curta"
        }

    password_hash = hash_password(password)

    query = """
    INSERT INTO users
    (name, email, phone, password_hash)

    VALUES
    (%s, %s, %s, %s)
    """

    try:
        db.execute_query(
            query,
            (
                name,
                email,
                phone,
                password_hash
            )
        )

        return {
            "success": True,
            "message": "Cadastro realizado com sucesso!"
        }

    except Exception:
        return {
            "success": False,
            "message": "Email já cadastrado! Tente novamente"
        }

# ___________________________________________________________________________
# LOGIN
def login_user_service(
    db,
    email,
    password
):

    query = """
    SELECT id, name, password_hash
    FROM users
    WHERE email = %s
    """

    result = db.execute_query(
        query,
        (email,)
    )

    if not result:
        return {
            "success": False,
            "message": "Usuário não encontrado! Tente novamente"
        }
    user_id, name, password_hash = result[0]

    if not check_password(
        password,
        password_hash
    ):

        return {
            "success": False,
            "message": "Senha incorreta! Tente novamente"
        }

    return {
        "success": True,
        "user": {
            "id": user_id,
            "name": name
        }
    }

# ___________________________________________________________________________
# PRIORIDADE
def calculate_priority(urgency, impact):

    total = urgency + impact

    if total <= 3:
        return "Baixa"
    elif total <= 7:
        return "Média"
    else:
        return "Alta"

# ___________________________________________________________________________
# CRIAR SOLICITAÇÃO
def create_request_service(
    db,
    user_id,
    category,
    description,
    urgency,
    impact
):

    priority = calculate_priority(
        urgency,
        impact
    )

    query = """
    INSERT INTO requests
    (
        user_id,
        category,
        description,
        urgency,
        impact,
        priority,
        status
    )

    VALUES
    (%s,%s,%s,%s,%s,%s,%s)
    """

    db.execute_query(
        query,
        (
            user_id,
            category,
            description,
            urgency,
            impact,
            priority,
            "Em aberto"
        )
    )

# ___________________________________________________________________________
# SOLICITAÇÕES POR USUÁRIO
def get_requests_by_user(
    db,
    user_id
):

    query = """
    SELECT
        category,
        description,
        priority,
        status,
        created_at

    FROM requests
    WHERE user_id = %s
    ORDER BY created_at DESC
    """

    return db.execute_query(
        query,
        (user_id,)
    )

# ___________________________________________________________________________
# LISTAR USUÁRIOS
def list_users_service(db):

    query = """
    SELECT id, name, email
    FROM users
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# TODAS SOLICITAÇÕES
def list_all_requests_service(db):

    query = """
    SELECT
        requests.id,
        users.name,
        requests.category,
        requests.description,
        requests.priority,
        requests.status,
        requests.created_at
    FROM requests
    JOIN users
    ON users.id = requests.user_id
    ORDER BY requests.created_at DESC
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# LISTAR POR STATUS
def list_requests_by_status_service(db):

    query = """
    SELECT
        requests.id,
        users.name,
        requests.category,
        requests.description,
        requests.priority,
        requests.status
    FROM requests
    JOIN users
    ON users.id = requests.user_id
    ORDER BY requests.status
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# LISTAR POR PRIORIDADE
def list_requests_by_priority_service(db):

    query = """
    SELECT
        requests.id,
        users.name,
        requests.category,
        requests.description,
        requests.priority,
        requests.status
    FROM requests
    JOIN users
    ON users.id = requests.user_id
    ORDER BY
    CASE
        WHEN requests.priority = 'Alta' THEN 1
        WHEN requests.priority = 'Media' THEN 2
        ELSE 3
    END
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# LISTAR POR USUÁRIO
def list_requests_by_user_service(db):

    query = """
    SELECT
        requests.id,
        users.name,
        requests.category,
        requests.description,
        requests.priority,
        requests.status
    FROM requests
    JOIN users
    ON users.id = requests.user_id
    ORDER BY users.name
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# ATUALIZAR STATUS
def update_request_status_service(
    db,
    request_id,
    new_status
):

    query = """
    SELECT status
    FROM requests
    WHERE id = %s
    """

    result = db.execute_query(
        query,
        (request_id,)
    )

    if not result:
        return {
            "success": False,
            "message": "Solicitação não encontrada"
        }
    current_status = result[0][0]

    if current_status == "Finalizada":
        return {
            "success": False,
            "message": "Não é permitido reabrir solicitações finalizadas"
        }
    update_query = """
    UPDATE requests
    SET status = %s
    WHERE id = %s
    """

    db.execute_query(
        update_query,
        (new_status, request_id)
    )

    return {
        "success": True
    }

# ___________________________________________________________________________
# ESTATÍSTICAS
# POR STATUS
def stats_by_status_service(db):

    query = """
    SELECT
        status,
        COUNT(*)
    FROM requests
    GROUP BY status
    """

    return db.execute_query(query)

# POR PRIORIDADE
def stats_by_priority_service(db):

    query = """
    SELECT
        priority,
        COUNT(*)
    FROM requests
    GROUP BY priority
    """

    return db.execute_query(query)

# ___________________________________________________________________________
# CANCELAR SOLICITAÇÃO
def cancel_request_service(
    db,
    request_id
):

    query = """
    SELECT status
    FROM requests
    WHERE id = %s
    """

    result = db.execute_query(
        query,
        (request_id,)
    )

    if not result:

        return {
            "success": False,
            "message": "Solicitação não encontrada!"
        }

    current_status = result[0][0]

    if current_status == "Finalizada":

        return {
            "success": False,
            "message": "Não é possível cancelar uma solicitação finalizada"
        }

    update_query = """
    UPDATE requests
    SET status = 'Cancelada'
    WHERE id = %s
    """

    db.execute_query(
        update_query,
        (request_id,)
    )

    return {
        "success": True,
        "message": "Solicitação cancelada com sucesso!"
    }

# ___________________________________________________________________________
# PESQUISAR SOLICITAÇÃO   
def search_requests_service(db, termo):

    query = """
    SELECT
        requests.id,
        users.name,
        requests.category,
        requests.description,
        requests.priority,
        requests.status
    FROM requests
    JOIN users
    ON users.id = requests.user_id
    WHERE requests.description LIKE %s
    """

    return db.execute_query(
        query,
        (f"%{termo}%",)
    )