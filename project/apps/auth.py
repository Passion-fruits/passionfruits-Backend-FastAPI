from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

from datetime import timedelta

from project.core.models import session
from project.core.schemas.auth import SignUp, GoogleOauth

from project.utils.auth import get_user_info, is_user, create_user, token_check

from project.config import GOOGLE_OAUTH2_PATH, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM


router = APIRouter()


@router.post("/auth", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def sign_up(body: SignUp, authorize: AuthJWT = Depends()):
    create_user(
        session=session,
        name=body.name,
        email=body.email,
        genre_list=body.user_genre
    )

    access_token = authorize.create_access_token(
        subject=body.email,
        algorithm=ALGORITHM,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = authorize.create_refresh_token(
        subject=body.email,
        algorithm=ALGORITHM,
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post(f"{GOOGLE_OAUTH2_PATH}", status_code=status.HTTP_200_OK, tags=["auth"])
async def google_login(body: GoogleOauth, authorize: AuthJWT = Depends()):
    email = get_user_info(id_token=body.id_token)

    if not is_user(session=session, email=email):
        return {
            "isFresh": True,
            "email": email
        }

    access_token = authorize.create_access_token(
        subject=email,
        algorithm=ALGORITHM,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = authorize.create_refresh_token(
        subject=email,
        algorithm=ALGORITHM,
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "isFresh": False,
        "email": email,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def token_refresh(authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="refresh")

    email = authorize.get_jwt_subject()

    access_token = authorize.create_access_token(
        subject=email,
        algorithm=ALGORITHM,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token
    }
