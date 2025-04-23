import bcrypt
from jose import JWTError, jwt
from app.core.config import settings
from fastapi import HTTPException

class Security:
    @staticmethod
    def hash_string(plain_text: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_text.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_hash(plain_text: str, hashed_text: str) -> bool:
        return bcrypt.checkpw(plain_text.encode("utf-8"), hashed_text.encode("utf-8"))
    
    @staticmethod
    def verify_refresh_token(refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
            return user_id
        except JWTError:
            print("JWTError:", JWTError)
            raise HTTPException(status_code=401, detail="Invalid refresh token")
