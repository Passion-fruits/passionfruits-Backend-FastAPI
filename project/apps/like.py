from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

from project.core.models import session

from project.utils.auth import token_check
from project.utils.like import like_it


router = APIRouter()


@router.post("/like/{song_id}", status_code=status.HTTP_201_CREATED, tags=["like"])
async def like(song_id: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    user_email = authorize.get_jwt_subject()

    like_it(session=session, user_email=user_email, song_id=song_id)

    return {
        "message": "success"
    }
