from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class User_like_playlist(Base):
    __tablename__ = "user_like_playlist"

    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    playlist = relationship("Playlist", backref=backref("playlist_liked"))
    user = relationship("User", backref=backref("user_like_playlist"))
