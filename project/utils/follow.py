from fastapi import HTTPException, status

from sqlalchemy import or_

from project.core.models import Session
from project.core.models.user import User
from project.core.models.follow import Follow

from project.utils.auth import is_user


def is_follow(session: Session, follower_id: int, following_id: int):
    follow_check = session.query(Follow).\
        filter(or_(Follow.follower == follower_id, Follow.following == following_id)).scalar()

    return True if follow_check else False


def get_user_id(session: Session, email: str):
    return session.query(User).filter(User.email == email).first().id


def follow_it(session: Session, follower_email: str, following_id: int):
    if not is_user(session=session, email=follower_email) or not is_user(session=session, user_id=following_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this email")

    follower_id = get_user_id(session=session, email=follower_email)
    if is_follow(session=session, follower_id=follower_id, following_id=following_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user is already follow")

    session.add(
        Follow(follower=follower_id, following=following_id)
    )
    session.commit()
