# main.py - Main entry point for the Request Tracker application
import logging
import os

from dotenv import load_dotenv

from database import Database, DatabaseError
from services import (
    create_request,
    list_requests,
    list_requests_by_priority,
    list_requests_by_status,
    list_requests_by_user,
    list_users,
    login_user,
    register_user,
    stats_by_priority,
    stats_by_status,
    update_request_status,
    cancelar_solicitacao,
)

load_dotenv()  # load environment variables from a .env file (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# Configure global logging settings: level, message format, and date/time.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


def get_env_or_raise(key: str) -> str:
    """Helper function for retrieving an environment variable, raising if missing."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente {key} não definida.")
    return value


# ========= UI helpers =========
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg: str = "Pressione ENTER para continuar...") -> None:
    input(f"\n{msg}")


def print_box(title: str, lines: list[str], width: int = 44) -> None:
    """Prints a simple boxed menu with a title."""
    width = max(width, len(title) + 6, *(len(line) + 4 for line in lines))
    border = "═" * width

    print(f"╔{border}╗")
    print(f"║ {title.center(width - 2)} ║")
    print(f"╠{border}╣")
    for line in lines:
        print(f"║ {line.ljust(width - 2)} ║")
    print(f"╚{border}╝")


def main_menu() -> None:
    clear_screen()
    print_box(
        "MENU PRINCIPAL",
        [
            "[1] Cadastrar usuário",
            "[2] Login",
            "[0] Sair",
        ],
    )


def logged_menu(user: dict) -> None:
    clear_screen()
    username = user.get("name", "Usuário")
    print_box(
        f"LOGADO COMO: {username}",
        [
            "[1] Cadastrar solicitação",
            "[2] Listar usuários",
            "[3] Listar solicitações (todas)",
            "[4] Listar por status",
            "[5] Listar por prioridade",
            "[6] Listar por usuário",
            "[7] Atualizar status",
            "[8] Estatísticas por status",
            "[9] Estatísticas por prioridade",
            "[10] Cancelar solicitação",
            "[0] Logout",
        ],
    )


def start_system() -> None:
    """Main function to start the system."""
    try:
        # Create the database instance using environment variables for connection parameters,
        # then create the necessary tables if they do not exist.
        db = Database(
            host=get_env_or_raise("DB_HOST"),
            user=get_env_or_raise("DB_USER"),
            password=get_env_or_raise("DB_PASSWORD"),
            database=get_env_or_raise("DB_NAME"),
        )

        # SQL query to create the users table if it does not exist
        create_user_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            phone VARCHAR(20)
        );
        """

        # SQL query to create the requests table if it does not exist
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

        # Use the database connection as a context manager
        with db:
            # Ensures that the tables exist
            db.execute_query(create_user_table_query)
            db.execute_query(create_request_table_query)

            # Stores the logged-in user (None = nobody logged in)
            logged_user = None

            while True:
                if not logged_user:
                    main_menu()
                    option = input("Escolha: ").strip()

                    if option == "1":
                        register_user(db)
                        pause()
                    elif option == "2":
                        logged_user = login_user(db)
                        pause()
                    elif option == "0":
                        break
                    else:
                        print("Opção inválida.")
                        pause()
                else:
                    logged_menu(logged_user)
                    option = input("Escolha: ").strip()

                    if option == "1":
                        create_request(db)
                        pause()
                    elif option == "2":
                        list_users(db)
                        pause()
                    elif option == "3":
                        list_requests(db)
                        pause()
                    elif option == "4":
                        list_requests_by_status(db)
                        pause()
                    elif option == "5":
                        list_requests_by_priority(db)
                        pause()
                    elif option == "6":
                        list_requests_by_user(db)
                        pause()
                    elif option == "7":
                        update_request_status(db)
                        pause()
                    elif option == "8":
                        stats_by_status(db)
                        pause()
                    elif option == "9":
                        stats_by_priority(db)
                        pause()
                    elif option == "10":
                        cancelar_solicitacao(db)
                        pause()
                    elif option == "0":
                        logged_user = None
                        print("Logout realizado.")
                        pause()
                    else:
                        print("Opção inválida.")
                        pause()

        logging.info("Sistema finalizado.")
    except (DatabaseError, ValueError) as error:
        logging.error(f"Erro ao iniciar o sistema: {error}")


if __name__ == "__main__":
    start_system()