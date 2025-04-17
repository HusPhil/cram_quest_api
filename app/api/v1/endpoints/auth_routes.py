from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.core.security import Security
from app.core.auth import create_access_token, create_refresh_token

from app.crud.player_crud import crud_create_player
from app.schemas.player_schema import PlayerCreate

from app.crud.profile_crud import crud_create_profile
from app.schemas.profile_schema import ProfileCreate

from app.crud.auth_crud import crud_sign_up_user
from app.schemas.auth_schema import SignUpRequest

from app.crud.user_crud import crud_read_user_by_username, crud_create_user
from app.models.user_model import User
from app.schemas.user_schema import UserRead

from jose import JWTError, jwt

refresh_token_cookie_key = "_Host-cramquest_ssfpwrtk"

router = APIRouter()

class InvalidCredential(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid username or password")


@router.post("/sign_in")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    
    try:
        user = await crud_read_user_by_username(session, username=form_data.username)
    except:
        raise InvalidCredential

    if not user:
        raise InvalidCredential
    
    if not Security.verify_hash(form_data.password, user.password):
        raise InvalidCredential

    response = _get_authentication_response(user)

    return response

@router.post("/sign_up")
async def sign_up(sign_up_request: SignUpRequest, session: Session = Depends(get_session)):
    print("user_create", sign_up_request)
    
    new_user = await crud_sign_up_user(session, sign_up_request)
    print(f"\n\n\n\n\n\n\n{new_user}\n\n\n\n\n\n\n")
    response = _get_authentication_response(new_user)
    return response 

@router.post("/sign_out")
async def sign_out():
    response = JSONResponse(content={"message": "Successfully signed out"})

    response.delete_cookie(
        key=refresh_token_cookie_key,
        secure=False,
        path="/",
        samesite="lax",
        httponly=True,
    )

    return response

@router.post("/refresh_token")
async def refresh_token(request: Request, response: Response):

    refresh_token = request.cookies.get(refresh_token_cookie_key)

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        user_id = Security.verify_refresh_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": user_id})
    return {"access_token": new_access_token}


def _get_authentication_response(user: UserRead) -> JSONResponse:
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response = JSONResponse(content={
        "message": "Sucessfully signed in",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
    })

    response.set_cookie(
        key=refresh_token_cookie_key,
        value=refresh_token,
        httponly=True,
        secure=not True,  # True in production with HTTPS
        samesite="lax",  # or "strict" or "none"
        path="/",        # Send this cookie to all routes
    )

    return response