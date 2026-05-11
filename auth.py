# auth.py - Authentication utilities for the Request Tracker application
import bcrypt
import re

EMAIL_REGEX = r"^(?=.{1,254}$)(?=.{1,64}@)[A-Za-z0-9]+(?:[._%+-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$" # regex pattern to validate email addresses (basic validation, can be improved for more complex cases)

# function to hash a password using bcrypt, which is a secure hashing algorithm designed for password hashing. It generates a salt and hashes the password with it, returning the hashed password as a string.
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
# function to check if a given password matches a previously hashed password. It takes the plain text password and the hashed password, encodes them to bytes, and uses bcrypt's checkpw function to verify if they match, returning True if they do and False otherwise.
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# function to validate if an email address is in a valid format using a regular expression. It returns True if the email matches the pattern and False otherwise.
def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

# function to validate if a password meets certain criteria (in this case, a minimum length of 6 characters). It returns True if the password is valid and False otherwise.
def is_valid_password(password: str) -> bool:
    return len(password) >= 6