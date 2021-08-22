from fastapi import APIRouter, status, Header

from typing import Optional

from project.core.models import session_scope

from project.utils.auth import token_check
from project.utils.like import like_it, unlike_it


router = APIRouter()


@router.post("/like/{song_id}", status_code=status.HTTP_201_CREATED, tags=["like"])
async def like(song_id: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorization, type="access")

        like_it(session=session, user_id=user_id, song_id=song_id)

        return {
            "message": "success"
        }


@router.delete("/like/{song_id}", status_code=status.HTTP_200_OK, tags=["like"])
async def unlike(song_id: int, Authorzation: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorzation, type="access")

        unlike_it(session=session, user_id=user_id, song_id=song_id)

        return {
            "message": "success"
        }
