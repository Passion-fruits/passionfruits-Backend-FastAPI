from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

from project.core.models import session

from project.utils.auth import token_check
from project.utils.follow import follow_it, unfollow_it


router = APIRouter()


@router.post("/follow/{user_id}", status_code=status.HTTP_201_CREATED, tags=["follow"])
async def follow(user_id: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    follower_email = authorize.get_jwt_subject()

    follow_it(session=session, follower_email=follower_email, following_id=user_id)

    return {
        "message": "success"
    }


@router.delete("/follow/{user_id}", status_code=status.HTTP_200_OK, tags=["follow"])
async def unfollow(user_id: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    follower_email = authorize.get_jwt_subject()

    unfollow_it(session=session, follower_email=follower_email, following_id=user_id)

    return {
        "message": "success"
    }


@router.get("/following/{user_id}")
async def get_following(user_id: int):
    return


@router.get("/follower/{user_id}")
async def get_follower(user_id: int):
    return
