# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pandas as pd
from typing import List, Dict, Optional

app = FastAPI(title="Movie Recommendation API")

# Data models
class MovieList(BaseModel):
    movies: List[str]

class RecommendationRequest(BaseModel):
    user_id: str
    count: int
user_df = pd.read_csv("./data/ml-latest-small/ratings.csv")
users_ids = user_df["userId"].unique().tolist()
users_ids = [str(i) for i in users_ids]

# Dummy database
user_movies_db = {
    "user001": [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "Fight Club"
    ],
    "user002": [
        "Inception",
        "Interstellar",
        "The Matrix",
        "Blade Runner 2049",
        "Arrival"
    ],
    "user003": [
        "The Lord of the Rings: The Fellowship of the Ring",
        "Star Wars: Episode V - The Empire Strikes Back",
        "Harry Potter and the Prisoner of Azkaban",
        "The Hobbit: An Unexpected Journey",
        "Dune"
    ],
    "user004": [
        "Titanic",
        "The Notebook",
        "Pride and Prejudice",
        "La La Land",
        "A Star Is Born"
    ],
    "user005": [
        "The Avengers",
        "Iron Man",
        "Black Panther",
        "Spider-Man: Into the Spider-Verse",
        "The Dark Knight Rises"
    ]
}

# Output of rec.sys for user of interest
recommendation_db = {
    "user001": [
        "The Godfather: Part II",
        "Goodfellas",
        "The Departed",
        "Se7en",
        "The Silence of the Lambs",
        "American History X",
        "Memento",
        "The Usual Suspects",
        "Léon: The Professional",
        "No Country for Old Men"
    ],
    "user002": [
        "2001: A Space Odyssey",
        "The Martian",
        "Ex Machina",
        "Eternal Sunshine of the Spotless Mind",
        "Solaris",
        "Moon",
        "District 9",
        "Her",
        "WALL-E",
        "Primer"
    ],
    "user003": [
        "The Lord of the Rings: The Two Towers",
        "The Lord of the Rings: The Return of the King",
        "Star Wars: Episode IV - A New Hope",
        "The Princess Bride",
        "Narnia: The Lion, the Witch and the Wardrobe",
        "Stardust",
        "Pan's Labyrinth",
        "Avatar",
        "Harry Potter and the Goblet of Fire",
        "Game of Thrones"
    ],
    "user004": [
        "Romeo + Juliet",
        "When Harry Met Sally",
        "Sleepless in Seattle",
        "Before Sunrise",
        "The Fault in Our Stars",
        "Eternal Sunshine of the Spotless Mind",
        "500 Days of Summer",
        "Silver Linings Playbook",
        "About Time",
        "The Shape of Water"
    ],
    "user005": [
        "Thor: Ragnarok",
        "Captain America: The Winter Soldier",
        "Guardians of the Galaxy",
        "Logan",
        "Deadpool",
        "Wonder Woman",
        "The Dark Knight",
        "Shazam!",
        "Doctor Strange",
        "Watchmen"
    ]
}

# API endpoints
@app.get("/")
async def root():
    return {"message": "Movie Recommendation API is running"}

@app.get("/users")
async def get_users():
    """Get list of all available user IDs"""
    # return {"users": list(user_movies_db.keys())}
    return {"users": users_ids}

@app.get("/user/{user_id}/movies", response_model=MovieList)
async def get_user_movies(user_id: str):
    """Get favorite movies for a specific user"""
    if user_id not in user_movies_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return {"movies": user_movies_db[user_id]}

@app.post("/recommendations", response_model=MovieList)
async def get_recommendations(request: RecommendationRequest):
    """Get movie recommendations for a user"""
    user_id = request.user_id
    count = request.count
    print(user_id, count)
    # Apply Recommendation Engine
    if user_id not in recommendation_db:
        raise HTTPException(status_code=404, detail=f"No recommendations for user {user_id}")
    
    # Limit recommendations to available count or requested count
    available_recommendations = recommendation_db[user_id]
    movies_to_return = available_recommendations[:min(count, len(available_recommendations))]
    
    return {"movies": movies_to_return}

if __name__ == "__main__":
    # Run the server
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)