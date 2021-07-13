from project.core.models import Session
from project.core.models.song import Song


def is_song(session: Session, song_id: int):
    song = session.query(Song).filter(Song.id == song_id).scalar()

    return True if song else False
