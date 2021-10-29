from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DATETIME
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class User_comment_song(Base):
    __tablename__ = "user_comment_song"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    content = Column(VARCHAR(200), nullable=False)
    created_at = Column(DATETIME(6), nullable=False, server_default="CURRENT_TIMESTAMP")

    user = relationship("User", backref=backref("user_comment"))
    song = relationship("Song", backref=backref("song_commented"))
