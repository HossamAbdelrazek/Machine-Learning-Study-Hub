import sys
import os
import pandas as pd
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QPushButton, QListWidget,
                             QLabel, QGroupBox, QSpinBox, QListWidgetItem)
from PyQt5.QtCore import Qt, QTimer
from Inference_classes import UserUserRecommender, ContentBasedRecommender, HybridRecommender

# Load metadata (for title lookup)
metadata_df = pd.read_csv("Data/Films_metadata.csv")

# Build recommenders
user_model = UserUserRecommender("Data/ratings.csv", "Data/movies.csv")
content_model = ContentBasedRecommender("Data/Films_metadata.csv", "Data/Genres_encoded.csv", "Data/ratings.csv")
hybrid = HybridRecommender(user_model, content_model, metadata_df)

# Load unique user IDs
ratings_df = pd.read_csv("Data/ratings.csv")
user_ids = ratings_df['userId'].unique()

# Build recommendation DB
RECOMMENDATION_JSON_PATH = "user_recommendations.json"

# Try loading the recommendations if the file exists
if os.path.exists(RECOMMENDATION_JSON_PATH):
    print("Found cached recommendation DB. Loading...")
    with open(RECOMMENDATION_JSON_PATH, "r", encoding="utf-8") as f:
        recommendation_db = json.load(f)
else:
    print("No cached recommendation DB found. Building new one...")
    recommendation_db = {}
    for user_id in user_ids:
        recs = hybrid.get_recs(user_id=user_id, n=20)
        movie_titles = recs['title'].dropna().tolist()
        recommendation_db[f"user{int(user_id):03d}"] = movie_titles
        print(f"User {user_id} recommendations built.")
    # Save the recommendation DB to a JSON file
    print("Recommendation DB built.")
    with open("user_recommendations.json", "w", encoding='utf-8') as f:
        json.dump(recommendation_db, f, indent=4, ensure_ascii=False)
    # Load ratings and metadata
ratings_df = pd.read_csv("Data/ratings.csv")
metadata_df = pd.read_csv("Data/Films_metadata.csv")

# Normalize column names for safety
ratings_df.columns = [col.lower() for col in ratings_df.columns]
metadata_df.columns = [col.lower() for col in metadata_df.columns]

# Ensure movie title is matched correctly
if 'movieid' not in metadata_df.columns:
    raise ValueError("Expected 'movieId' column in metadata file.")

# Merge to get movie titles
merged_df = pd.merge(ratings_df, metadata_df[['movieid', 'title']], on='movieid', how='left')

# Drop 0.0 or NaN ratings (unrated)
merged_df = merged_df[merged_df['rating'] > 0.0]

# Create top-5 list per user
top_movies_per_user = {}

for user_id, group in merged_df.groupby('userid'):
    top_movies = (
        group.sort_values(by='rating', ascending=False)
             .drop_duplicates(subset='movieid')
             .head(5)['title']
             .dropna()
             .tolist()
    )
    top_movies_per_user[f"user{int(user_id):03d}"] = top_movies
class UserMoviesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()
        
    def initUI(self):
        self.setWindowTitle('User Movies Recommendation System')
        self.setGeometry(100, 100, 800, 500)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create user selection area
        selection_group = QGroupBox("User Selection")
        selection_layout = QHBoxLayout()
        
        # Create user ID combobox
        self.user_combo = QComboBox()
        self.user_combo.setMinimumWidth(150)
        
        # Create show button
        self.show_button = QPushButton("Show User Movies")
        self.show_button.clicked.connect(self.showUserMovies)
        
        # Add widgets to selection layout
        selection_layout.addWidget(QLabel("Select User ID:"))
        selection_layout.addWidget(self.user_combo)
        selection_layout.addWidget(self.show_button)
        selection_layout.addStretch()
        selection_group.setLayout(selection_layout)
        
        # Create recommendation controls
        recommendation_group = QGroupBox("Recommendation Controls")
        recommendation_layout = QHBoxLayout()
        
        # Create number of recommendations spinbox
        recommendation_layout.addWidget(QLabel("Number of recommendations:"))
        self.num_recommendations = QSpinBox()
        self.num_recommendations.setMinimum(1)
        self.num_recommendations.setMaximum(20)
        self.num_recommendations.setValue(5)
        recommendation_layout.addWidget(self.num_recommendations)
        
        # Create get recommendations button
        self.recommend_button = QPushButton("Get Movie Recommendations")
        self.recommend_button.clicked.connect(self.getRecommendations)
        recommendation_layout.addWidget(self.recommend_button)
        
        recommendation_layout.addStretch()
        recommendation_group.setLayout(recommendation_layout)
        
        # Create movies display area
        display_group = QGroupBox("Movies")
        display_layout = QHBoxLayout()
        
        # Create user movies area
        user_movies_layout = QVBoxLayout()
        user_movies_layout.addWidget(QLabel("User's Favorite Movies:"))
        self.user_movies_list = QListWidget()
        user_movies_layout.addWidget(self.user_movies_list)
        
        # Create recommended movies area
        recommended_layout = QVBoxLayout()
        recommended_layout.addWidget(QLabel("Recommended Movies:"))
        self.recommended_list = QListWidget()
        recommended_layout.addWidget(self.recommended_list)
        
        # Add both areas to display layout
        display_layout.addLayout(user_movies_layout)
        display_layout.addLayout(recommended_layout)
        display_group.setLayout(display_layout)
        
        # Add all components to main layout
        main_layout.addWidget(selection_group)
        main_layout.addWidget(recommendation_group)
        main_layout.addWidget(display_group)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
    def loadData(self):
        self.user_data = top_movies_per_user
        self.recommendation_db = recommendation_db
        # Populate user combobox
        for user_id in self.user_data.keys():
            self.user_combo.addItem(user_id)
    
    def showUserMovies(self):
        # Get selected user ID
        selected_user = self.user_combo.currentText()
        
        # Display user's favorite movies
        user_movies = self.user_data.get(selected_user, [])
        self.user_movies_list.clear()
        for movie in user_movies:
            item = QListWidgetItem(movie)
            self.user_movies_list.addItem(item)
        
        # Clear recommended movies area
        self.recommended_list.clear()
    
    def getRecommendations(self):
        # Get selected user ID and number of recommendations
        selected_user = self.user_combo.currentText()
        num_movies = self.num_recommendations.value()
        
        # Show loading message
        self.recommended_list.clear()
        loading_item = QListWidgetItem("Connecting to recommendation server...")
        self.recommended_list.addItem(loading_item)
        processing_item = QListWidgetItem("Processing request...")
        self.recommended_list.addItem(processing_item)
        
        # Simulate server request delay
        QTimer.singleShot(1500, lambda: self.displayRecommendations(selected_user, num_movies))
    
    def displayRecommendations(self, user_id, num_movies):
        # In a real application, this would make an API call to a recommendation engine
        # For now, we'll use our dummy database
        recommended_movies = self.recommendation_db.get(user_id, [])
        
        # Clear list widget
        self.recommended_list.clear()
        
        if not recommended_movies:
            self.recommended_list.addItem(QListWidgetItem("No recommendations available for this user."))
            return
        
        # Ensure we don't request more movies than available
        num_to_show = min(num_movies, len(recommended_movies))
        
        # Display recommendations
        header_item = QListWidgetItem(f"Top {num_to_show} Recommended Movies for {user_id}:")
        header_item.setFlags(Qt.ItemIsEnabled)  # Make it non-selectable
        self.recommended_list.addItem(header_item)
        
        for i in range(num_to_show):
            movie_item = QListWidgetItem(f"{i+1}. {recommended_movies[i]}")
            self.recommended_list.addItem(movie_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserMoviesApp()
    ex.show()
    sys.exit(app.exec_())