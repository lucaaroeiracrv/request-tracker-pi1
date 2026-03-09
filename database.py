# database.py

import mysql.connector
from mysql.connector import Error

# This class is responsible for managing the database connection and executing queries.
class Database:
    # The constructor initializes the database connection parameters and sets the connection to None.
    def __init__(self, host, user, password, database):
        self.host = host # The hostname of the database server
        self.user = user # The username to connect to the database
        self.password = password # The password to connect to the database  
        self.database = database # The name of the database to connect to
        self.connection = None # The connection object that will be used to interact with the database

    # This method establishes a connection to the database using the provided credentials.
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database                
            )
            # If the connection is successful, it prints a confirmation message.
            if self.connection.is_connected():
                print("Connected to the database")
        except Error as error:
            print(f"Error while connecting to MySQL: {error}")
    # This method closes the database connection if it is currently open.
    def disconnect(self): 
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from the database")
    # This method executes a given SQL query and returns the results. It checks if the connection is active before executing the query.
    def executeQuery(self, query, values=None):
        if not self.connection or not self.connection.is_connected(): 
            print("Not connected to the database")
            return None
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(query, values) # Executes the query with the provided values (if any)
            
            # If the query is a SELECT statement, it fetches and returns the results.
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit() # Commits the transaction for non-SELECT queries
                print("Query executed successfully")
                return None
            
        except Error as error:
            print(f"Error while executing query: {error}")
            return None
        
        finally:
            cursor.close() # Closes the cursor after executing the query
              