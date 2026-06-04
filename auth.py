import bcrypt
import re

EMAIL_REGEX = r"^(?=.{1,254}$)(?=.{1,64}@)[A-Za-z0-9]+(?:[._%+-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    ).decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )

def is_valid_email(email: str) -> bool:
    return re.match(
        EMAIL_REGEX,
        email
    ) is not None

def is_valid_password(password: str) -> bool:
    return len(password) >= 6