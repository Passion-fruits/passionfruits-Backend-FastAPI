from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.orm import aliased

from project.core.models import Session
from project.core.models.user import User
from project.core.models.profile import Profile
from project.core.models.follow import Follow

from project.utils.auth import is_user

from project.config import LIMIT_NUM


def is_follow(session: Session, follower_id: int, following_id: int):
    follow_check = session.query(Follow).\
        filter(Follow.follower == follower_id, Follow.following == following_id).scalar()

    return True if follow_check else False


def get_user_id(session: Session, email: str):
    return session.query(User).filter(User.email == email).first().id


def follow_it(session: Session, follower_email: str, following_id: int):
    if not is_user(session=session, email=follower_email) or not is_user(session=session, user_id=following_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this email")

    follower_id = get_user_id(session=session, email=follower_email)
    if is_follow(session=session, follower_id=follower_id, following_id=following_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user is already followed")

    session.add(
        Follow(follower=follower_id, following=following_id)
    )
    session.commit()


def unfollow_it(session: Session, follower_email: str, following_id: int):
    if not is_user(session=session, email=follower_email) or not is_user(session=session, user_id=following_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this")

    follower_id = get_user_id(session=session, email=follower_email)
    if not is_follow(session=session, follower_id=follower_id, following_id=following_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user is not followed")

    del_follow = session.query(Follow).filter(Follow.follower == follower_id, Follow.following == following_id).first()
    session.delete(del_follow)
    session.commit()


def get_followings(session: Session, user_id: int, page: int):
    if not is_user(session=session, user_id=user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this id")

    limit = LIMIT_NUM
    offset = page * limit

    Follow1 = aliased(Follow)
    Follow2 = aliased(Follow)

    following_info = session.query(
        Follow1.following,
        Profile.name,
        Profile.image_path,
        func.count(Follow2.follower).label("follower")
    ).join(Profile,  Follow1.following == Profile.user_id).\
        join(Follow2, Follow1.following == Follow2.following).\
        filter(Follow1.follower == 22).\
        group_by(Follow1.following, Profile.name, Profile.image_path).\
        order_by("follower").\
        limit(limit).offset(offset).all()

    return following_info
