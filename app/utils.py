from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])


# gerado de senha com hash
def hash_password(password: str):
    return crypt_context.hash(password)


def hash_verify_password(db_password: str, password: str):
    return crypt_context.verify(db_password, password)
