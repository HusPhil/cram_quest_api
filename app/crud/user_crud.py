from sqlmodel import Session, select
from app.models.user_model import User
from app.core.security import Security
from app.schemas.user_schema import UserRead

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

def get_user(session: Session, user_id: int) -> UserRead:
    user = session.get(User, user_id)

    if not user:
        return None

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email
    )

def get_all_users(session: Session) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return [
        UserRead(
            id=user.id,
            username=user.username,
            email=user.email
        )
        for user in users
    ]
