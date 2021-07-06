from fastapi import HTTPException

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests

from project.core.models import Session
from project.core.models.user import User

from project.config import CLIENT_ID


def get_user_info(id_token: str):
    idinfo = verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)

    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(status_code=400, detail="Unable to validate social login")

    if idinfo["email"] and idinfo["email_verified"]:
        email = idinfo.get("email")
    else:
        raise HTTPException(status_code=400, detail="Unable to validate social login")

    return email


def is_user(session: Session, email: str):
    user = session.query(User).filter(User.email == email).scalar()

    return True if user else False
