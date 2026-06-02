# main.py - Main entry point for the Request Tracker application
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
    cancelar_solicitacao,
)

load_dotenv() # load environment variables from a .env file (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) 

# configure global logging settings, defines the level, message format, and date/time.
logging.basicConfig(
    level=logging.INFO, # set the logging level to INFO, which means that all messages at this level and above (WARNING, ERROR, CRITICAL) will be logged.
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s" 
)

def get_env_or_raise(key: str) -> str: # helper function for retrieving an environment variable.
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente {key} não definida.") # throws an error if the variable does not exist.
    return value


def main_menu(): # function to display the main menu options for the user when they are not logged in.
    print("\n===== MENU =====")
    print("1 - Cadastrar usuário")
    print("2 - Login")
    print("0 - Sair")

def logged_menu(user): # function to display the menu options for the user when they are logged in
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
    print("10 - Cancelar solicitação")
    print("0 - Logout")

def start_system(): # main function to start the system
    try:
        # create the database instance using environment variables for connection parameters, then create the necessary tables if they do not exist.
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

        with db:# use the database connection as a context manager
            # ensures that the tables exist
            db.execute_query(create_user_table_query)
            db.execute_query(create_request_table_query)

            # stores the logged-in user (None = nobody logged in)
            logged_user = None
            while True: # main loop
                if not logged_user: # if no user is logged in, show the main menu
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
                else: # if a user is logged in, show the logged-in menu with more options
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
                    elif option == "10":
                        id_chamado = input("Digite o ID do chamado a cancelar: ").strip()
                        if id_chamado.isdigit():
                            cancelar_solicitacao(db, int(id_chamado))
                        else:
                            print("ID do chamado inválido. Digite um número.")
                    elif option == "0":
                        logged_user = None
                        print("Logout realizado.")
                    else:
                        print("Opção inválida.")

        logging.info("Sistema finalizado.")
    except (DatabaseError, ValueError) as error:
        logging.error(f"Erro ao iniciar o sistema: {error}")

if __name__ == "__main__": # ensures that the system will only start if this file is executed directly.
    start_system()