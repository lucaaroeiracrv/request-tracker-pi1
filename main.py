import logging
import os
from dotenv import load_dotenv
from database import Database, DatabaseError
from services import (
    register_user,
    login_user,
    create_request,
    list_users,
    list_requests,
    list_requests_by_status,
    list_requests_by_priority,
    list_requests_by_user,
    update_request_status,
    stats_by_status,
    stats_by_priority,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

def get_env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente {key} não definida.")
    return value

def main_menu():
    print("\n===== MENU =====")
    print("1 - Cadastrar usuário")
    print("2 - Login")
    print("0 - Sair")

def logged_menu(user):
    print(f"\n===== LOGADO COMO {user['name']} =====")
    print("1 - Cadastrar solicitação")
    print("2 - Listar usuários")
    print("3 - Listar solicitações (todas)")
    print("4 - Listar por status")
    print("5 - Listar por prioridade")
    print("6 - Listar por usuário")
    print("7 - Atualizar status")
    print("8 - Estatísticas por status")
    print("9 - Estatísticas por prioridade")
    print("0 - Logout")

def start_system():
    try:
        db = Database(
            host=get_env_or_raise("DB_HOST"),
            user=get_env_or_raise("DB_USER"),
            password=get_env_or_raise("DB_PASSWORD"),
            database=get_env_or_raise("DB_NAME"),
        )

        create_user_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            phone VARCHAR(20)
        );
        """

        create_request_table_query = """
        CREATE TABLE IF NOT EXISTS requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            urgency TINYINT NOT NULL,
            impact TINYINT NOT NULL,
            priority VARCHAR(10) NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

        with db:
            db.execute_query(create_user_table_query)
            db.execute_query(create_request_table_query)

            logged_user = None
            while True:
                if not logged_user:
                    main_menu()
                    option = input("Escolha: ").strip()

                    if option == "1":
                        register_user(db)
                    elif option == "2":
                        logged_user = login_user(db)
                    elif option == "0":
                        break
                    else:
                        print("Opção inválida.")
                else:
                    logged_menu(logged_user)
                    option = input("Escolha: ").strip()

                    if option == "1":
                        create_request(db)
                    elif option == "2":
                        list_users(db)
                    elif option == "3":
                        list_requests(db)
                    elif option == "4":
                        list_requests_by_status(db)
                    elif option == "5":
                        list_requests_by_priority(db)
                    elif option == "6":
                        list_requests_by_user(db)
                    elif option == "7":
                        update_request_status(db)
                    elif option == "8":
                        stats_by_status(db)
                    elif option == "9":
                        stats_by_priority(db)
                    elif option == "0":
                        logged_user = None
                        print("Logout realizado.")
                    else:
                        print("Opção inválida.")

        logging.info("Sistema finalizado.")
    except (DatabaseError, ValueError) as error:
        logging.error(f"Erro ao iniciar o sistema: {error}")

if __name__ == "__main__":
    start_system()