from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserRead
from app.schemas.auth_schema import SignUpRequest
from fastapi import HTTPException
from app.models import User, Player, Profile  # Adjust paths

from app.core.security import Security

async def crud_sign_up_user(session: AsyncSession, sign_up_data: SignUpRequest) -> UserRead:
    try:
        # Create User
        new_user = User(
            username=sign_up_data.username,
            email=sign_up_data.email,
            password=Security.hash_string(sign_up_data.password)
        )
        session.add(new_user)
        await session.flush()  # populate new_user.id

        # Create Player
        new_player = Player(user_id=new_user.id)
        session.add(new_player)
        await session.flush()  # populate new_player.id

        # Create Profile
        new_profile = Profile(player_id=new_player.id, avatar_url=sign_up_data.avatar_url)
        session.add(new_profile)

        # Finalize
        await session.commit()
        await session.refresh(new_user)

        print("\n\n\n\n\n\n\nSUCESSFULL REGISTRATION\n\n\n\n\n\n\n")

        return UserRead(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email
        )  # or _serialize_user(new_user)

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
