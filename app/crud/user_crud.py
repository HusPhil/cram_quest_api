from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.user_model import User
from app.core.security import Security
from app.schemas.user_schema import UserRead, UserUpdate
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

def crud_update_user(session: Session, user_id: int, user_update: UserUpdate) -> UserRead:
    """Update a User while preventing duplicate usernames/emails and ensuring partial updates."""
    
    # ✅ Fetch the User and Check for Duplicates in ONE Query
    statement = (
        select(User)
        .where((User.id == user_id) | (((User.username == user_update.username) | (User.email == user_update.email)) & (User.id != user_id)))
    )

    results = session.exec(statement).all()  # ✅ Only ONE database call

    # ✅ Extract User & Potential Duplicate from the same result set
    user = next((row for row in results if row.id == user_id), None)
    existing_user = next((row for row in results if row.id != user_id), None)

    if not user:
        raise UserNotFound(f"User with ID {user_id} not found.")

    if existing_user:
        raise UserAlreadyExists(f"Username or email already in use by another user.")

    update_data = {}

    if user_update.username is not None:
        update_data["username"] = user_update.username
    if user_update.email is not None:
        update_data["email"] = user_update.email
    if user_update.password:
        update_data["password"] = Security.hash_string(user_update.password.get_secret_value())

    if not update_data:
        return UserRead(id=user.id, username=user.username, email=user.email)  # ✅ No Updates, Return Existing Data

    try:
        for key, value in update_data.items():
            setattr(user, key, value)

        session.commit()
        session.refresh(user)

        return UserRead(id=user.id, username=user.username, email=user.email)  # ✅ Single Return Statement

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def crud_delete_user(session: Session, user_id: int) -> UserRead:
    try:

        # 🔍 Retrieve the user
        user = session.get(User, user_id)
        if not user:
            session.rollback()
            raise UserNotFound

        session.delete(user)

        # ✅ Explicitly commit transaction
        session.commit()

        return UserRead(
            id=user.id,
            username=user.username,
            email=user.email
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    




