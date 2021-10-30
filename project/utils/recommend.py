import pandas as pd

from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize

from random import choice, sample

from sqlalchemy.orm import Session


def recommend_ids_by_collaborative_filtering(session: Session, song_id: int, size: int):
    like = pd.read_sql_query("SELECT * FROM user_like_song;", session.bind)
    like["is_like"] = 1

    comment = pd.read_sql_query("SELECT user_id, song_id FROM user_comment_song;", session.bind)
    comment["is_comment"] = 1

    user_score = pd.merge(like, comment, how='outer', on=['user_id', 'song_id'])
    user_score.fillna(0, inplace=True)
    user_score['score'] = user_score['is_like'] + user_score['is_comment']
    user_score.drop(['is_like', 'is_comment'], axis=1, inplace=True)

    score_matrix = user_score.pivot_table(values='score', index='song_id', columns='user_id')
    score_matrix.fillna(0, inplace=True)

    song_similarity = linear_kernel(score_matrix, score_matrix)
    recommendation = pd.DataFrame(data=song_similarity, index=score_matrix.index, columns=score_matrix.index)

    if not song_id:
        song_id = choice(recommendation.index)

    recommend_ids = list(recommendation[song_id].sort_values(ascending=False)[:size].index)

    return recommend_ids


def recommend_ids_by_nmf(session: Session, song_id: int, size: int):
    songs = pd.read_sql_query(
        "SELECT A.id AS song_id, B.genre_type_id AS genre, C.mood_type_id AS mood "
        "FROM song A "
        "JOIN song_genre B ON A.id = B.song_id "
        "JOIN mood C ON A.id = C.song_id;",
        session.bind
    )
    song_info = songs[["genre", "mood"]]

    nmf = NMF(n_components=2)
    nmf_feature = nmf.fit_transform(song_info)
    normal_feature = normalize(nmf_feature)

    nmf_df = pd.DataFrame(normal_feature)
    joined_df = nmf_df.join(songs.song_id)
    pivot_df = pd.pivot_table(joined_df, joined_df[[0, 1]], ["song_id"])

    value = pivot_df.loc[song_id]
    similarities = pivot_df.dot(value)

    sorted_similarities = similarities.nlargest(len(similarities))
    recommended_ids = list(sorted_similarities[sorted_similarities.map(lambda x: x>=0.85)].index)

    return sample(recommended_ids, size)
