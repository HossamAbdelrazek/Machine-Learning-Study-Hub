import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

class UserUserRecommender:
    def __init__(self, ratings_path, movies_path=None):
        # Load ratings and replace 0.0 with NaN
        self.ratings_df = pd.read_csv(ratings_path)
        self.ratings_df['rating'] = self.ratings_df['rating'].replace(0.0, np.nan)
        if movies_path:
            self.movies_df = pd.read_csv(movies_path)
        else:
            self.movies_df = None

        # Create user-item matrix
        self.user_item_matrix = self.ratings_df.pivot_table(index='userId', columns='movieId', values='rating')

        # Fill NaNs with 0 for similarity computation
        self.user_item_matrix_filled = self.user_item_matrix.fillna(0)

        # Compute user-user similarity
        self.user_similarity_df = pd.DataFrame(
            cosine_similarity(self.user_item_matrix_filled),
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )

    def predict_rating(self, user_id, movie_id, k=5):
        if movie_id not in self.user_item_matrix.columns:
            return np.nan

        similarities = self.user_similarity_df.loc[user_id]
        ratings = self.user_item_matrix[movie_id]

        data = pd.concat([similarities, ratings], axis=1)
        data.columns = ['similarity', 'rating']
        data = data.dropna()
        data = data[data['rating'] > 0.0]

        if data.empty:
            return np.nan

        top_k = data.sort_values('similarity', ascending=False).head(k)

        if top_k['similarity'].sum() == 0:
            return np.nan

        pred = np.dot(top_k['similarity'], top_k['rating']) / top_k['similarity'].sum()
        return pred

    def get_recs(self, user_id, n=10):
        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"User ID {user_id} not found.")

        rated_movies = self.user_item_matrix.loc[user_id].dropna().index
        unrated_movies = list(set(self.user_item_matrix.columns) - set(rated_movies))

        predictions = []
        for movie_id in unrated_movies:
            pred = self.predict_rating(user_id, movie_id, k=3)
            if not np.isnan(pred):
                predictions.append((movie_id, pred))

        top_n = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]

        if self.movies_df is not None:
            top_n_df = pd.DataFrame(top_n, columns=['movieId', 'predicted_rating'])
            merged = top_n_df.merge(self.movies_df, on='movieId')
            return merged[['movieId', 'title', 'predicted_rating']]
        else:
            return pd.DataFrame(top_n, columns=['movieId', 'predicted_rating'])


class ContentBasedRecommender:
    def __init__(self, metadata_path, genres_path, ratings_path):
        self.metadata_path = metadata_path
        self.genres_path = genres_path
        self.ratings_path = ratings_path

        self.merged_df = None
        self.similarity_df = None
        self.ratings_df = None

        self._load_and_prepare_data()
        self._compute_similarity_matrix()
        self._load_ratings()

    def _load_and_prepare_data(self):
        films_df = pd.read_csv(self.metadata_path)
        genres_df = pd.read_csv(self.genres_path)

        self.merged_df = pd.merge(films_df, genres_df, on='Unnamed: 0')
        self.merged_df.set_index('movieID', inplace=True)


        columns_to_drop = ['Unnamed: 0', 'genres', 'imdb_link', 'tmdb_link']
        self.merged_df.drop(columns=[col for col in columns_to_drop if col in self.merged_df.columns], inplace=True)


        self.merged_df['title'] = self.merged_df['title'].astype(str)

    def _compute_similarity_matrix(self):
        non_feature_cols = ['title']  
        genre_features = self.merged_df.drop(columns=non_feature_cols, errors='ignore')

        similarity_matrix = cosine_similarity(genre_features)
        self.similarity_df = pd.DataFrame(
            similarity_matrix,
            index=self.merged_df.index,
            columns=self.merged_df.index
        )

    def _load_ratings(self):
        self.ratings_df = pd.read_csv(self.ratings_path)
        self.ratings_df.columns = [col.lower() for col in self.ratings_df.columns]
        self.ratings_df['rating'] = self.ratings_df['rating'].astype(float).replace(0.0, pd.NA)

    def get_recs(self, movie_id, n=10):
        if movie_id not in self.similarity_df:
            raise ValueError(f"Movie ID {movie_id} not found in similarity matrix.")

        sim_scores = self.similarity_df[movie_id].sort_values(ascending=False)
        sim_scores = sim_scores.drop(movie_id)

        top_n_ids = sim_scores.head(n).index
        recs = self.merged_df.loc[top_n_ids][['title']].copy()
        recs['movieId'] = top_n_ids
        recs['similarity_score'] = sim_scores.loc[top_n_ids].values

        return recs[['movieId', 'title', 'similarity_score']].reset_index(drop=True)

    def get_user_recs(self, user_id, n=10, top_rated=3):
        if user_id not in self.ratings_df['userid'].unique():
            raise ValueError(f"User ID {user_id} not found in ratings data.")

        user_ratings = self.ratings_df[self.ratings_df['userid'] == user_id]
        user_ratings = user_ratings.dropna(subset=['rating'])
        user_rated_ids = set(user_ratings['movieid'])

        top_movies = user_ratings.sort_values(by='rating', ascending=False)['movieid'].tolist()[:top_rated]

        all_recs = pd.DataFrame()

        for movie_id in top_movies:
            if movie_id in self.similarity_df:
                recs = self.get_recs(movie_id, n=n * 2)
                all_recs = pd.concat([all_recs, recs], ignore_index=True)

        all_recs.drop_duplicates(subset='movieId', inplace=True)
        all_recs = all_recs[~all_recs['movieId'].isin(user_rated_ids)]

        return all_recs.sort_values(by='similarity_score', ascending=False).head(n).reset_index(drop=True)

    def get_cleaned_dataframe(self):
        return self.merged_df.copy()
    
    

class HybridRecommender:
    def __init__(self, user_model, content_model, metadata_df):
        """
        :param user_model: UserUserRecommender instance
        :param content_model: ContentBasedRecommender instance
        :param metadata_df: DataFrame with global metadata including 'movieId' and 'users_avg_ratings_to_movie'
        """
        self.user_model = user_model
        self.content_model = content_model
        self.metadata_df = metadata_df.copy()
        self.metadata_df.columns = [col.lower() for col in self.metadata_df.columns]

    def get_recs(self, user_id, n=20):
        user_recs = self.user_model.get_recs(user_id, n=n)
        content_recs = self.content_model.get_user_recs(user_id, n=n)

        user_recs = user_recs.rename(columns={'predicted_rating': 'user_score'})
        content_recs = content_recs.rename(columns={'similarity_score': 'content_score'})

        combined = pd.concat([user_recs[['movieId']], content_recs[['movieId']]], ignore_index=True)
        combined = combined.drop_duplicates(subset='movieId')

        if 'movieid' in self.metadata_df.columns:
            self.metadata_df = self.metadata_df.rename(columns={'movieid': 'movieId'})

        merged = combined.merge(
            self.metadata_df[['movieId', 'title', 'users_avg_ratings_to_movie']],
            on='movieId', how='left'
        )

        merged = merged.sort_values(by='users_avg_ratings_to_movie', ascending=False)


        return merged.head(n).reset_index(drop=True)

