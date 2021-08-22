from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from project.core.models.user_like_song import User_like_song

from project.utils.song import is_song


def is_like(session: Session, user_id: int, song_id: int):
    like = session.query(User_like_song).\
        filter(User_like_song.user_id == user_id, User_like_song.song_id == song_id).scalar()

    return True if like else False


def like_it(session: Session, user_id: int, song_id: int):

    if not is_song(session=session, song_id=song_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find song matching this id")

    if is_like(session=session, user_id=user_id, song_id=song_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user already like this song")

    session.add(
        User_like_song(user_id=user_id, song_id=song_id)
    )
    session.commit()


def unlike_it(session: Session, user_id: int, song_id: int):

    if not is_song(session=session, song_id=song_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find song matching this id")

    if not is_like(session=session, user_id=user_id, song_id=song_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user does not like this song")

    del_like = session.query(User_like_song).\
        filter(User_like_song.user_id == user_id, User_like_song.song_id == song_id).first()

    session.delete(del_like)
    session.commit()
