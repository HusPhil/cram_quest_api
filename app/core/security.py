import bcrypt

class Security:
    @staticmethod
    def hash_string(plain_text: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_text.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_hash(plain_text: str, hashed_text: str) -> bool:
        return bcrypt.checkpw(plain_text.encode("utf-8"), hashed_text.encode("utf-8"))
