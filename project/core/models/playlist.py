from sqlalchemy import Column, Integer, VARCHAR, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(30), nullable=False)
    cover_url = Column(VARCHAR(255))
    created_at = Column(DATETIME, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", backref=backref("user_playlist"))
