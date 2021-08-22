from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.orm import aliased, Session

from project.core.models.profile import Profile
from project.core.models.follow import Follow

from project.utils import is_user

from project.config import LIMIT_NUM


def is_follow(session: Session, follower_id: int, following_id: int):
    follow_check = session.query(Follow).\
        filter(Follow.follower == follower_id, Follow.following == following_id).scalar()

    return True if follow_check else False


def follow_it(session: Session, follower_id: int, following_id: int):
    if not is_user(session=session, user_id=follower_id) or not is_user(session=session, user_id=following_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this email")

    if is_follow(session=session, follower_id=follower_id, following_id=following_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this user is already followed")

    session.add(
        Follow(follower=follower_id, following=following_id)
    )
    session.commit()


def unfollow_it(session: Session, follower_id: int, following_id: int):
    if not is_user(session=session, user_id=follower_id) or not is_user(session=session, user_id=following_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this")

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
        func.count(Follow2.follower)
    ).join(Profile,  Follow1.following == Profile.user_id).\
        join(Follow2, Follow1.following == Follow2.following).\
        filter(Follow1.follower == 22).\
        group_by(Follow1.following, Profile.name, Profile.image_path).\
        order_by(func.count(Follow2.follower).desc()).\
        limit(limit).offset(offset).all()

    return following_info


def get_followers(session: Session, user_id: int, page: int):
    if not is_user(session=session, user_id=user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this id")

    limit = LIMIT_NUM
    offset = page * limit

    Follow1 = aliased(Follow)
    Follow2 = aliased(Follow)

    follower_info = session.query(
        Follow1.follower,
        Profile.name,
        Profile.image_path,
        func.count(Follow2.follower)
    ).join(Profile, Follow1.follower == Profile.user_id). \
        outerjoin(Follow2, Follow1.follower == Follow2.following). \
        filter(Follow1.following == 22). \
        group_by(Follow1.follower, Profile.name, Profile.image_path). \
        order_by(func.count(Follow2.follower).desc()). \
        limit(limit).offset(offset).all()

    return follower_info
