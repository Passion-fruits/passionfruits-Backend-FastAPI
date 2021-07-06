from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT

from datetime import timedelta

from project.core.models import session
from project.core.schemas.auth import GoogleOauth

from project.utils.auth import get_user_info, is_user

from project.config import GOOGLE_OAUTH2_PATH, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM


router = APIRouter()


@router.post(f"{GOOGLE_OAUTH2_PATH}", tags=["auth"])
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
