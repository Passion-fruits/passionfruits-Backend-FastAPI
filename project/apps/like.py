from fastapi import APIRouter, status, Header

from typing import Optional

from project.core.models import session_scope

from project.utils.auth import token_check
from project.utils.like import like_song, unlike_song, is_like_song


router = APIRouter()


@router.post("/like/song/{song_id}", status_code=status.HTTP_201_CREATED, tags=["like"])
async def user_like_song(song_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorization, type="access")

        like_song(session=session, user_id=user_id, song_id=song_id)

        return {
            "message": "success"
        }


@router.delete("/like/song/{song_id}", status_code=status.HTTP_200_OK, tags=["like"])
async def user_unlike_song(song_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorization, type="access")

        unlike_song(session=session, user_id=user_id, song_id=song_id)

        return {
            "message": "success"
        }


@router.get("/like", status_code=status.HTTP_200_OK, tags=["like"])
async def is_like_song(song_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorization, type="access")

        return {
            "is_like": is_like_song(session=session, user_id=user_id, song_id=song_id)
        }
