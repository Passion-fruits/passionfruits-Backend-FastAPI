from sqlalchemy.orm import Session

from project.core.models.user import User


def is_user(session: Session, email: str = None, user_id: int = None):
    if email and not user_id:
        user = session.query(User).filter(User.email == email)

        if user.scalar():
            return user.first().id
        else:
            return None

    elif not email and user_id:
        user = session.query(User).filter(User.id == user_id)

        if user.scalar():
            return user.first().id
        else:
            return None
