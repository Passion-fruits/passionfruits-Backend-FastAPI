from fastapi import HTTPException, status

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests

from sqlalchemy import or_
from sqlalchemy.orm import Session

from datetime import datetime

from project.core.models.user import User
from project.core.models.profile import Profile
from project.core.models.user_genre import User_genre
from project.core.models.genre_type import Genre_type
from project.core.models.sns import Sns

from project.utils import is_user
from project.utils.kdt import get_random_wallet

from project.config import CLIENT_ID, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


def get_user_info(id_token: str):
    idinfo = verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)

    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate social login")

    if idinfo["email"] and idinfo["email_verified"]:
        email = idinfo.get("email")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate social login")

    return email


def create_user(session: Session, name: str, email: str, genre_list: list, image_path: str):
    if is_user(session=session, email=email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already in use")

    private_key, wallet = get_random_wallet()

    user = User(
        email=email,
        private_key=private_key
    )

    profile = Profile(
        name=name,
        image_path=image_path,
        wallet=wallet
    )

    genre_filter_options = [Genre_type.name.like(genre_name) for genre_name in genre_list]
    genre_queries = session.query(Genre_type).filter(or_(*genre_filter_options)).all()
    genre_ids = [q.id for q in genre_queries]

    profile.user_genres = [User_genre(genre_type_id=genre_id) for genre_id in genre_ids]
    profile.sns = [Sns()]

    user.profiles = [profile]

    session.add(user)
    session.flush()

    user_id = user.id

    session.commit()

    return user_id


def create_token(user_id: int, type: str):
    return encode(
        payload={
            "sub": user_id,
            "type": type,
            "iat": datetime.utcnow(),
            "exp": (datetime.utcnow()+(ACCESS_TOKEN_EXPIRE_MINUTES if type == "access" else REFRESH_TOKEN_EXPIRE_MINUTES))
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM,
        headers={
            "typ": "JWT",
            "alg": ALGORITHM
        }
    )


def token_check(token: str, type: str):
    try:
        payload = decode(token[7:], SECRET_KEY, algorithms=[ALGORITHM])
        if (payload["type"] == type):
            return payload["sub"]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token is required")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
