from fastapi import APIRouter, status, Header

from typing import Optional

from project.core.models import session_scope

from project.utils.auth import token_check
from project.utils.follow import follow_it, unfollow_it, get_followings, get_followers, is_follow


router = APIRouter()


@router.post("/follow/{user_id}", status_code=status.HTTP_201_CREATED, tags=["follow"])
async def follow(user_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        following_id = token_check(token=Authorization, type="access")

        follow_it(session=session, follower_id=user_id, following_id=following_id)

        return {
            "message": "success"
        }


@router.delete("/follow/{user_id}", status_code=status.HTTP_200_OK, tags=["follow"])
async def unfollow(user_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        following_id = token_check(token=Authorization, type="access")

        unfollow_it(session=session, follower_id=user_id, following_id=following_id)

        return {
            "message": "success"
        }


@router.get("/following/{user_id}", status_code=status.HTTP_200_OK, tags=["follow"])
async def get_following(user_id: int, page: int):
    with session_scope() as session:
        followings = get_followings(session=session, user_id=user_id, page=page)

        return {
            "followings": [{
                "id": id,
                "name": name,
                "image_path": image_path,
                "follower": follower
            } for id, name, image_path, follower in followings]
        }


@router.get("/follower/{user_id}", status_code=status.HTTP_200_OK, tags=["follow"])
async def get_follower(user_id: int, page: int):
    with session_scope() as session:
        followers = get_followers(session=session, user_id=user_id, page=page)

        return {
            "followers": [{
                "id": id,
                "name": name,
                "image_path": image_path,
                "follower": follower
            } for id, name, image_path, follower in followers]
        }


@router.get("/follow", status_code=status.HTTP_200_OK, tags=["follow"])
async def is_follows(user_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        following_id = token_check(token=Authorization, type="access")

        return {
            "is_follow": is_follow(session=session, follower_id=user_id, following_id=following_id)
        }
