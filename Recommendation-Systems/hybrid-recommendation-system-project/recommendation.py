import pandas as pd


def get_user_ids():
    user_df = pd.read_csv("./data/ml-latest-small/ratings.csv")
    users_ids = user_df["userId"].unique().tolist()
    return [str(i) for i in users_ids]

def get_user_movies():
    return {
        "1": [
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

def get_user_recommendations():
    return{
        "1": [
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