from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Song_genre(Base):
    __tablename__ = "song_genre"

    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    genre_type_id = Column(Integer, ForeignKey("genre_type.id"), primary_key=True)

    song = relationship("Song", backref=backref("song_genre"))
    genre_type = relationship("Genre_type", backref=backref("genre_song"))
