from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class User_like_song(Base):
    __tablename__ = "user_like_song"

    user_id = Column(Integer, ForeignKey("user.id"))
    song_id = Column(Integer, ForeignKey("song.id"))

    user = relationship("User", backref=backref("user_like"))
    song = relationship("Song", backref=backref("song_liked"))
