from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Mood(Base):
    __tablename__ = "mood"

    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    mood_type_id = Column(Integer, ForeignKey("mood_type.id"), primary_key=True)

    song = relationship("Song", backref=backref("song_mood"))
    mood_type = relationship("Mood_type", backref=backref("mood_song"))
