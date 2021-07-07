from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class User_genre(Base):
    __tablename__ = "user_genre"

    profile_user_id = Column(Integer, ForeignKey("profile.user_id"))
    genre_type_id = Column(Integer, ForeignKey("genre_type.id"))

    profile = relationship("Profile", backref=backref("user_genres"))
    genre_type = relationship("Genre_type", backref("genre_types"))
