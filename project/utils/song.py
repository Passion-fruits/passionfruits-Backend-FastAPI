from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.orm import Session

from project.core.models.song import Song
from project.core.models.profile import Profile
from project.core.models.user_like_song import User_like_song
from project.core.models.user_comment_song import User_comment_song
from project.core.models.song_genre import Song_genre
from project.core.models.genre_type import Genre_type
from project.core.models.mood import Mood
from project.core.models.mood_type import Mood_type
from project.core.models.history import History
from project.core.models.follow import Follow


def is_song(session: Session, song_id: int):
    song = session.query(Song).filter(Song.id == song_id).scalar()

    return True if song else False


def get_lits_by_ids(session: Session, song_ids: list):
    songs = session.query(
        Song.id,
        Song.title,
        Song.description,
        Genre_type.name,
        Song.created_at,
        Song.short_url,
        Song.cover_url,
        Song.user_id,
        Profile.name,
        func.count(User_like_song.user_id),
        func.count(User_comment_song.user_id)
    ).join(Profile, Song.user_id == Profile.user_id).\
        outerjoin(User_like_song, Song.id == User_like_song.song_id).\
        outerjoin(User_comment_song, Song.id == User_comment_song.song_id).\
        join(Song_genre, Song.id == Song_genre.song_id).\
        join(Genre_type, Song_genre.genre_type_id == Genre_type.id).\
        filter(Song.id.in_(song_ids)).\
        group_by(
        Song.id,
        Song.title,
        Song.description,
        Genre_type.name,
        Song.short_url,
        Song.cover_url,
        Song.user_id,
        Profile.name
    )

    return songs


def get_songs_by_ids(session: Session, song_ids: list):
    songs = session.query(
        Song.id,
        Song.title,
        Song.user_id,
        Profile.name,
        Song.song_url,
        Song.cover_url,
        func.count(User_like_song.user_id)
    ).join(Profile, Song.user_id == Profile.user_id).\
        outerjoin(User_like_song, Song.id == User_like_song.song_id).\
        filter(Song.id.in_(song_ids)).\
        group_by(
        Song.id,
        Song.title,
        Song.user_id,
        Profile.name,
        Song.song_url,
        Song.cover_url
    )

    return songs


def get_playlist_by_ids(session: Session, song_ids: list):
    songs = session.query(
        Song.id,
        Song.title,
        Genre_type.name,
        Mood_type.name,
        Song.created_at,
        Song.user_id,
        Profile.name,
        Song.song_url,
        Song.cover_url,
        func.count(User_like_song.user_id)
    ).join(Profile, Song.user_id == Profile.user_id).\
        outerjoin(User_like_song, Song.id == User_like_song.song_id). \
        join(Song_genre, Song.id == Song_genre.song_id).\
        join(Genre_type, Song_genre.genre_type_id == Genre_type.id).\
        join(Mood, Song.id == Mood.song_id).\
        join(Mood_type, Mood.mood_type_id == Mood_type.id).\
        filter(Song.id.in_(song_ids)).\
        group_by(
        Song.id,
        Song.title,
        Genre_type.name,
        Genre_type.name,
        Mood_type.name,
        Song.created_at,
        Song.user_id,
        Profile.name,
        Song.song_url,
        Song.cover_url
    )

    return songs


def get_user_history(session: Session, user_id: int, size: int):
    song_ids = session.query(
        History.song_id
    ).filter(History.user_id == user_id).\
        order_by(History.created_at.desc()).\
        limit(size).all()

    if not song_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user has no history")

    return song_ids


def get_following_songs(session: Session, user_id: int, page: int, size: int):
    limit = size
    offset = (page - 1) * limit

    songs = session.query(
        Song.id,
        Song.user_id,
        Song.cover_url,
        Song.song_url,
        Song.title,
        Profile.name,
        func.count(User_like_song.user_id)
    ).join(Profile, Song.user_id == Profile.user_id).\
        join(Follow, Follow.following == user_id).\
        outerjoin(User_like_song, Song.id == User_like_song.song_id).\
        filter(Song.user_id == Follow.follower).\
        group_by(
        Song.id,
        Song.user_id,
        Song.cover_url,
        Song.song_url,
        Song.title,
        Profile.name
    ).order_by(Song.created_at.desc()).\
    limit(limit).offset(offset).all()

    return songs
