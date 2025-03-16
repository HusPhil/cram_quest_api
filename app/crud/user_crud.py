from sqlmodel import Session, select
from app.models.user_model import User
from app.core.security import Security

def create_user(session: Session, username: str, email: str, password: str) -> User:
    
    hashed_password = Security.hash_string(password)

    db_user = User(
        username=username, 
        email=email, 
        password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session):
    return session.exec(select(User)).all()
