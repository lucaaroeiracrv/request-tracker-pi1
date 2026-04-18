# database.py - Database management for the Request Tracker application
import logging
from typing import Any, Iterable, Optional
import mysql.connector
from mysql.connector import Error, MySQLConnection

logger = logging.getLogger(__name__) # logger configuration should be done in the main application entry point

class DatabaseError(Exception): # create a custom exception for database errors
    """Erro genérico de banco de dados."""
    pass

class Database: # class to manage database connections and queries
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        # Initialize the database connection parameters
        self.host = host
        self.user = user
        self.password = password    
        self.database = database
        self.connection: Optional[MySQLConnection] = None # initialize the connection attribute to None

    def connect(self) -> None: # method to establish a connection to the database
        try: 
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            if self.connection.is_connected(): # check if the connection was successful
                logger.info("Connected to the database")
            else: # if the connection is not successful, raise a custom DatabaseError
                raise DatabaseError("Failed to connect to the database") 
        except Error as error: # catch any MySQL errors and log them, then raise a custom DatabaseError with the error message
            logger.exception("Erro ao conectar ao MySQL")
            raise DatabaseError(str(error)) from error

    def disconnect(self) -> None: # method to close the database connection
        if self.connection and self.connection.is_connected():# check if the connection exists and is open before trying to close it
            self.connection.close()
            logger.info("Disconnected from the database")
            
    # method to execute a SQL query with optional parameters  (SELECT, INSERT, UPDATE, DELETE, etc.)
    def execute_query(self, query: str, values: Optional[Iterable[Any]] = None): 
        if not self.connection or not self.connection.is_connected(): # check if the connection is established before trying to execute a query, if not raise a custom DatabaseError
            raise DatabaseError("Não está conectado ao banco de dados")

        cursor = self.connection.cursor() # create a cursor object to execute the SQL query

        try:
            cursor.execute(query, values) # executes the query, with optional values ​​(prevents SQL Injection).

            if query.strip().upper().startswith("SELECT"): # if the query is a SELECT statement, fetch and return the results, otherwise commit the transaction and return None
                return cursor.fetchall()
            else: # for non-SELECT queries, commit the transaction to save changes to the database
                self.connection.commit()
                logger.info("Query executada com sucesso")
                return None

        except Error as error: # catch any MySQL errors that occur during query execution, log them, and raise a custom DatabaseError with the error message
            logger.exception("Erro ao executar a query")
            raise DatabaseError(str(error)) from error

        finally: # ensure that the cursor is closed after the query execution, regardless of success or failure
            cursor.close()

    def __enter__(self): # implement the context manager protocol to allow using the Database class with a 'with' statement, which ensures that the connection is properly opened and closed
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb): # when exiting the 'with' block, whether an exception occurred or not, the database connection will be closed by calling
        self.disconnect()