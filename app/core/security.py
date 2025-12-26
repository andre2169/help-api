from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    # bcrypt aceita no máximo 72 bytes
    return pwd_context.hash(password[:72])
