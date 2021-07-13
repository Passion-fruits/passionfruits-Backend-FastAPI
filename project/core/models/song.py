from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cover_url = Column(VARCHAR(150), nullable=False)
    title = Column(VARCHAR(30), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    song_url = Column(VARCHAR(150), nullable=False)
    short_url = Column(VARCHAR(150), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", backref=backref("songs"))
