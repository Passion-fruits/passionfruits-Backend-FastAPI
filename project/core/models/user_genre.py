from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class User_genre(Base):
    __tablename__ = "user_genre"

    profile_user_id = Column(Integer, ForeignKey("profile.user_id"), primary_key=True)
    genre_type_id = Column(Integer, ForeignKey("genre_type.id"), primary_key=True)

    profile = relationship("Profile", backref=backref("user_genres"))
    genre_type = relationship("Genre_type", backref=backref("genre_types"))
