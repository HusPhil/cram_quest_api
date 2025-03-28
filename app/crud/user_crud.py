from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import User
from app.core.security import Security
from app.schemas.user_schema import UserRead, UserUpdate, UserCreate

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User with the same username or email already exists")


async def crud_create_user(session: AsyncSession, user_create: UserCreate) -> UserRead:
    
    _check_existing_user_based_on_email_and_username(session, user_create.username, user_create.email)

    hashed_password = Security.hash_string(user_create.password.get_secret_value())

    new_user = User(
        username=user_create.username, 
        email=user_create.email, 
        password=hashed_password
    )

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return _serialize_user(new_user)
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists

async def crud_read_user_by_id(session: AsyncSession, user_id: int) -> UserRead:
    user = await _get_user_or_404(session, user_id)
    return _serialize_user(user)

async def crud_read_user_by_username(session: AsyncSession, username: str) -> User:
    """ used in authentication """
    
    result = await session.execute(
        select(User)
        .where(User.username == username)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound

    return user

async def crud_read_all_users(session: AsyncSession) -> list[UserRead]:
    result = await session.execute(select(User))
    
    users = result.scalars().all()

    return [_serialize_user(user) for user in users]

async def crud_update_user(session: AsyncSession, user_id: int, user_update: UserUpdate) -> UserRead:
    """Update a User while preventing duplicate usernames/emails and ensuring partial updates."""
    
    user = await _get_user_or_duplicate_error(session, user_id, user_update)

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

        await session.commit()
        await session.refresh(user)

        return _serialize_user(user)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected SQLAlchemyError: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def crud_delete_user(session: AsyncSession, user_id: int) -> UserRead:
    try:
        user = await _get_user_or_404(session, user_id)

        await session.delete(user)
        await session.commit()
        
        return _serialize_user(user)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    

async def _get_user_or_duplicate_error(session: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    statement = (
        select(User)
        .where(
            (User.id == user_id) | 
            (
                ((User.username == user_update.username) | (User.email == user_update.email)) & 
                (User.id != user_id)
            )
        )
    )

    results = await session.execute(statement)  
    results = results.scalars().all()

    # ✅ Extract User & Potential Duplicate from the same result set

    user = next((row for row in results if row.id == user_id), None)
    if not user:
        raise UserNotFound

    existing_user = next((row for row in results if row.id != user_id), None)
    if existing_user:
        raise UserAlreadyExists

    return user

async def _get_user_or_404(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise UserNotFound
    return user

async def _check_existing_user_based_on_email_and_username(session: AsyncSession, email: str, username: str) -> None:
    result = await session.execute(
        select(User.id)
        .where((User.username == username) | (User.email == email))
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise UserAlreadyExists

def _serialize_user(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email
    )


