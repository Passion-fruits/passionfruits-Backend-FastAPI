from sqlalchemy import func, and_
from sqlalchemy.orm import Session, aliased

from project.core.models.playlist import Playlist
from project.core.models.profile import Profile
from project.core.models.user_like_playlist import User_like_playlist


def is_playlist(session: Session, playlist_id: int):
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id).scalar()

    return True if playlist else False


def get_like_playlists(session: Session, user_id: int, page: int, size: int):
    limit = size
    offset = (page - 1) * limit

    Like1 = aliased(User_like_playlist)
    Like2 = aliased(User_like_playlist)

    playlists = session.query(
        Playlist.id,
        Playlist.name,
        Playlist.cover_url,
        Profile.name,
        func.count(Like2.user_id)
    ).join(Profile, Playlist.user_id == Profile.user_id)\
        .join(Like1, and_(Like1.user_id == user_id, Playlist.id == Like1.playlist_id))\
        .outerjoin(Like2, Playlist.id == Like2.playlist_id)\
        .group_by(
        Playlist.id,
        Playlist.name,
        Playlist.cover_url,
        Profile.name
    )\
        .limit(limit).offset(offset).all()

    return playlists
