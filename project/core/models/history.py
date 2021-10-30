from sqlalchemy import Column, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class History(Base):
    __tablename__ = "history"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    created_at = Column(DATETIME(6), nullable=False, server_default="CURRENT_TIMESTAMP")

    user = relationship("User", backref=backref("user_listen"))
    song = relationship("Song", backref=backref("song_listened"))
