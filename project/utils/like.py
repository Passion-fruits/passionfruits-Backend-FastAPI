from fastapi import HTTPException, status

from project.core.models import Session
from project.core.models.user_like_song import User_like_song

from project.utils import get_user_id
from project.utils.song import is_song


def like_it(session: Session, user_email: str, song_id: int):
    user_id = get_user_id(session=session, email=user_email)

    if not is_song(session=session, song_id=song_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find song matching this id")

    session.add(
        User_like_song(user_id=user_id, song_id=song_id)
    )
    session.commit()
