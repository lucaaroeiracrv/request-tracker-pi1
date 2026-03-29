import logging
import os
from dotenv import load_dotenv
from database import Database, DatabaseError
from services import register_user, login_user

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
    print("9 - Logout")

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
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            phone VARCHAR(20)
        );
        """

        with db:
            db.execute_query(create_user_table_query)

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
                    if option == "9":
                        logged_user = None
                        print("Logout realizado.")
                    else:
                        print("Opção inválida.")

        logging.info("Sistema finalizado.")
    except (DatabaseError, ValueError) as error:
        logging.error(f"Erro ao iniciar o sistema: {error}")

if __name__ == "__main__":
    start_system()