# main.py   

from database import Database
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def startSystem():
    # Create an instance of the Database class with the appropriate connection parameters.
    db = Database(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    db.connect()
    
    print("Welcome to the system!")
    
    # Define the SQL query to create the users table if it does not already exist. 
    createUserTableQuery = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phone VARCHAR(20)
        );
        """
        
        # Execute the query to create the users table in the database.
    db.executeQuery(createUserTableQuery)
        
    print("Users table created successfully.")
        
    db.disconnect()

# The main entry point of the program. When the script is run directly, it calls the startSystem function to initialize the system and manage the database connection.       
if __name__ == "__main__":
    startSystem()