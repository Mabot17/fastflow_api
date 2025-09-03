from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class Hash:

    def pbkdf2_sha256(password: str):
        return pwd_context.hash(secret=password)

    def verify(hashed_password: str, plain_password: str):
        return pwd_context.verify(secret=plain_password, hash=hashed_password)
