from fastapi import HTTPException, status

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests

from sqlalchemy import or_

from project.core.models import Session
from project.core.models.user import User
from project.core.models.profile import Profile
from project.core.models.user_genre import User_genre
from project.core.models.genre_type import Genre_type

from project.config import CLIENT_ID


def get_user_info(id_token: str):
    idinfo = verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)

    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate social login")

    if idinfo["email"] and idinfo["email_verified"]:
        email = idinfo.get("email")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate social login")

    return email


def is_user(session: Session, email: str = None, user_id: int = None, raise_exception: bool = False):
    if email and not user_id:
        user = session.query(User).filter(User.email == email).scalar()

        return True if user else False

    elif not email and user_id:
        user = session.query(User).filter(User.id == user_id).scalar()

        return True if user else False


def create_user(session: Session, name: str, email: str, genre_list: list):
    if is_user(session=session, email=email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")

    user = User(email=email)

    profile = Profile(name=name)

    genre_filter_options = [Genre_type.name.like(genre_name) for genre_name in genre_list]
    genre_queries = session.query(Genre_type).filter(or_(*genre_filter_options)).all()
    genre_ids = [q.id for q in genre_queries]

    profile.user_genres = [User_genre(genre_type_id=genre_id) for genre_id in genre_ids]

    user.profiles = [profile]

    session.add(user)
    session.commit()
