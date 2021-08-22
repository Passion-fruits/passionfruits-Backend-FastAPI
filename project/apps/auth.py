from fastapi import APIRouter, status, Header

from typing import Optional

from project.core.models import session_scope
from project.core.schemas.auth import SignUp, GoogleOauth

from project.utils.auth import get_user_info, is_user, create_user, token_check, create_token

from project.config import GOOGLE_OAUTH2_PATH


router = APIRouter()


@router.post("/auth", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def sign_up(body: SignUp):
    with session_scope() as session:
        user_id = create_user(
            session=session,
            name=body.name,
            email=body.email,
            genre_list=body.user_genre,
            image_path=body.image_path
        )

        access_token = create_token(
            user_id=user_id,
            type="access"
        )
        refresh_token = create_token(
            user_id=user_id,
            type="refresh"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


@router.post(f"{GOOGLE_OAUTH2_PATH}", status_code=status.HTTP_200_OK, tags=["auth"])
async def google_login(body: GoogleOauth):
    with session_scope() as session:
        email = get_user_info(id_token=body.id_token)

        if not (user_id := is_user(session=session, email=email)):
            return {
                "isFresh": True,
                "email": email
            }

        access_token = create_token(
            user_id=user_id,
            type="access"
        )
        refresh_token = create_token(
            user_id=user_id,
            type="refresh"
        )

        return {
            "isFresh": False,
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token
        }


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def token_refresh(Authorization: Optional[str] = Header(...)):
    user_id = token_check(token=Authorization, type="refresh")

    access_token = create_token(
        user_id=user_id,
        type="access"
    )

    return {
        "access_token": access_token
    }
