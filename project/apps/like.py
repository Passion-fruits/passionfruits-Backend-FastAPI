from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

from project.core.models import session_scope

from project.utils.auth import token_check
from project.utils.like import like_it, unlike_it


router = APIRouter()


@router.post("/like/{song_id}", status_code=status.HTTP_201_CREATED, tags=["like"])
async def like(song_id: int, authorize: AuthJWT = Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")

        user_email = authorize.get_jwt_subject()

        like_it(session=session, user_email=user_email, song_id=song_id)

        return {
            "message": "success"
        }


@router.delete("/like/{song_id}", status_code=status.HTTP_200_OK, tags=["like"])
async def unlike(song_id: int, authorize: AuthJWT = Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")

        user_email = authorize.get_jwt_subject()

        unlike_it(session=session, user_email=user_email, song_id=song_id)

        return {
            "message": "success"
        }
