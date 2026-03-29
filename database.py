import logging
from typing import Any, Iterable, Optional
import mysql.connector
from mysql.connector import Error, MySQLConnection

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Erro genérico de banco de dados."""
    pass

class Database:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[MySQLConnection] = None

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            if self.connection.is_connected():
                logger.info("Connected to the database")
            else:
                raise DatabaseError("Failed to connect to the database")
        except Error as error:
            logger.exception("Erro ao conectar ao MySQL")
            raise DatabaseError(str(error)) from error

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Disconnected from the database")

    def execute_query(self, query: str, values: Optional[Iterable[Any]] = None):
        if not self.connection or not self.connection.is_connected():
            raise DatabaseError("Não está conectado ao banco de dados")

        cursor = self.connection.cursor()

        try:
            cursor.execute(query, values)

            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                logger.info("Query executada com sucesso")
                return None

        except Error as error:
            logger.exception("Erro ao executar a query")
            raise DatabaseError(str(error)) from error

        finally:
            cursor.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()