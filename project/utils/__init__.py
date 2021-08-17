from sqlalchemy.orm import Session

from project.core.models.user import User


def is_user(session: Session, email: str = None, user_id: int = None):
    if email and not user_id:
        user = session.query(User).filter(User.email == email).scalar()

        return True if user else False

    elif not email and user_id:
        user = session.query(User).filter(User.id == user_id).scalar()

        return True if user else False


def get_user_id(session: Session, email: str):
    return session.query(User).filter(User.email == email).first().id
