from auth import hash_password, check_password, is_valid_email, is_valid_password

def register_user(db):
    name = input("Nome: ").strip()
    email = input("Email: ").strip()
    phone = input("Telefone (opcional): ").strip()
    password = input("Senha (mín. 6 caracteres): ").strip()

    if not name:
        print("Nome é obrigatório.")
        return
    if not is_valid_email(email):
        print("Email inválido.")
        return
    if not is_valid_password(password):
        print("Senha muito curta.")
        return

    password_hash = hash_password(password)

    query = """
        INSERT INTO users (name, email, phone, password_hash)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute_query(query, (name, email, phone, password_hash))
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")

def login_user(db):
    email = input("Email: ").strip()
    password = input("Senha: ").strip()

    query = "SELECT id, name, password_hash FROM users WHERE email = %s"
    result = db.execute_query(query, (email,))

    if not result:
        print("Usuário não encontrado.")
        return None

    user_id, name, password_hash = result[0]

    if check_password(password, password_hash):
        print(f"Login OK! Bem-vindo, {name}")
        return {"id": user_id, "name": name, "email": email}
    else:
        print("Senha incorreta.")
        return None