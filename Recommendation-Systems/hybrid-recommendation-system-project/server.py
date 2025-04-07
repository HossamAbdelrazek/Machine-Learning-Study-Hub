# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pandas as pd
from typing import List, Dict, Optional
from recommendation import get_user_movies, get_user_recommendations, get_user_ids

app = FastAPI(title="Movie Recommendation API")

# Data models
class MovieList(BaseModel):
    movies: List[str]

class RecommendationRequest(BaseModel):
    user_id: str
    count: int

users_ids = get_user_ids()

# Dummy database
user_movies_db = get_user_movies()

# Output of rec.sys for user of interest
recommendation_db = get_user_recommendations()

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