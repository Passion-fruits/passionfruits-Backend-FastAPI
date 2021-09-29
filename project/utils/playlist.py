from sqlalchemy.orm import Session

from project.core.models.playlist import Playlist


def is_playlist(session: Session, playlist_id: int):
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id).scalar()

    return True if playlist else False
