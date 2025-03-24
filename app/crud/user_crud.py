from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.user_model import User
from app.core.security import Security
from app.schemas.user_schema import UserRead
from typing import Optional

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists")

def crud_create_user(session: Session, username: str, email: str, password: str) -> UserRead:
    
    existing_user = session.exec(
        select(User.id).where((User.username == username) | (User.email == email))
    ).first()

    if existing_user:
        raise UserAlreadyExists

    hashed_password = Security.hash_string(password)

    db_user = User(
        username=username, 
        email=email, 
        password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserRead(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )

def crud_read_user_by_id(session: Session, user_id: int) -> UserRead:
    user = session.get(User, user_id)

    if not user:
        raise UserNotFound

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email
    )

def crud_read_user_by_username(session: Session, username: str) -> User:
    
    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        raise UserNotFound

    return user

def crud_read_all_users(session: Session) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return [
        UserRead(
            id=user.id,
            username=user.username,
            email=user.email
        )
        for user in users
    ]

def crud_update_user(session: Session, user_id: int, username: str, email: str, password: Optional[str]) -> UserRead:
    user = session.get(User, user_id)

    if not user:
        raise UserNotFound
    
    # 🔍 Check if another user has the same username/email
    existing_user = session.exec(
        select(User).where(
            ((User.username == username) | (User.email == email)) & (User.id != user_id)
        )
    ).first()

    if existing_user:
        raise UserAlreadyExists  # ❌ Prevents duplicate usernames/emails
    
    if not (username or email or password):
        return UserRead(
            id=user.id,
            username=user.username,
            email=user.email
        )

    update_data = {
        "username": username,
        "email": email
    }

    if password:
        print("this has been called")
        update_data["password"] = Security.hash_string(password)

    try:
        for key, value in update_data.items():
            setattr(user, key, value)

        session.commit()
        session.refresh(user)

        return UserRead(
            id=user.id,
            username=user.username,        
            email=user.email
        )
        
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def crud_delete_user(session: Session, user_id: int) -> UserRead:
    user = session.get(User, user_id)

    if not user:
        raise UserNotFound

    session.delete(user)
    session.commit()

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email
    )