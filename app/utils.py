from passlib.context import CryptContext

# initializes an instance (handling password hashing and verification)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashes user password
def hash(password: str):
    return pwd_context.hash(password)


# Compares current password used for log in with the one in database
# (already hashed)
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
