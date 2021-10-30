from fastapi import APIRouter, status, Header

from typing import Optional

from datetime import datetime

from pytz import timezone

from project.core.models import session_scope

from project.utils.auth import token_check
from project.utils.recommend import recommend_ids_by_collaborative_filtering, recommend_ids_by_nmf
from project.utils.song import get_lits_by_ids, get_songs_by_ids, get_playlist_by_ids, get_user_history


router = APIRouter()


@router.get("/recommend/lit", status_code=status.HTTP_200_OK, tags=["recommendation"])
async def get_lit_recommendation(song_id: int, size: int):
    with session_scope() as session:
        recommended_ids = recommend_ids_by_collaborative_filtering(session=session, song_id=song_id, size=size)
        recommended_lits = get_lits_by_ids(session=session, song_ids=recommended_ids)

        return [{
            "song_id": id,
            "title": title,
            "description": description,
            "genre": genre,
            "created_at": created_at,
            "short_url": short_url,
            "cover_url": cover_url,
            "user_id": user_id,
            "artist": name,
            "like": like,
            "comment": comment
        } for id, title, description, genre, created_at, short_url, cover_url, user_id, name, like, comment in recommended_lits]


@router.get("/recommend/song/detail", status_code=status.HTTP_200_OK, tags=["recommendation"])
async def get_similar_songs_in_main(song_id: int, size: int):
    with session_scope() as session:
        recommended_ids = recommend_ids_by_nmf(session=session, song_id=song_id, size=size)
        recommended_songs = get_songs_by_ids(session=session, song_ids=recommended_ids)

        return [{
            "song_id": id,
            "title": title,
            "user_id": user_id,
            "artist": name,
            "song_url": song_url,
            "cover_url": cover_url,
            "like": like
        } for id, title, user_id, name, song_url, cover_url, like in recommended_songs]


@router.get("/recommend/main/playlist", status_code=status.HTTP_200_OK, tags=["recommendation"])
async def get_similar_songs_in_main(song_id: int, size: int):
    with session_scope() as session:
        recommended_ids = recommend_ids_by_nmf(session=session, song_id=song_id, size=size)
        songs = get_playlist_by_ids(session=session, song_ids=recommended_ids)

        return {
            "name": None,
            "author": "KUNDER",
            "like": 0,
            "cover_url": None,
            "playlist_id": 0,
            "created_at": datetime.now(timezone("Asia/Seoul")),
            "songs": [{
                "song_id": id,
                "title": title,
                "genre": genre,
                "mood": mood,
                "created_at": created_at,
                "user_id": user_id,
                "artist": name,
                "song_url": song_url,
                "cover_url": cover_url,
                "like": like
            } for id, title, genre, mood, created_at, user_id, name, song_url, cover_url, like in songs]
        }


@router.get("/recommend/main", status_code=status.HTTP_200_OK, tags=["recommendation"])
async def get_recent_songs_in_main(size: int, Authorization: Optional[str] = Header(...)):
    with session_scope() as session:
        user_id = token_check(token=Authorization, type="access")
        song_ids = get_user_history(session=session, user_id=user_id, size=size)

        return [{
            "playlist_id": 0,
            "name": f"데일리 추천{i}",
            "cover_url": f"/rPlaylist{i}.png",
            "like": None,
            "base_song_id": song_ids[i-1]["song_id"]
        } for i in range(1, size+1)]
