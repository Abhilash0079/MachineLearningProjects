import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OMDB_API_KEY")

# search_terms = [
#     "action",
#     "comedy",
#     "drama",
#     "thriller",
#     "romance",
#     "horror",
#     "crime",
#     "mystery",
#     "adventure",
#     "fantasy",
#     "animation",
#     "superhero",
#     "batman",
#     "marvel",
#     "dc",
#     "star",
#     "harry",
#     "mission",
#     "matrix",
#     "jurassic"
# ]

search_terms = [
    "spy",
    "war",
    "bollywood",
    "hollywood",
    "biography",
    "history",
    "political",
    "musical",
    "family",
    "western",
    "sports",
    "disaster",
    "zombie",
    "vampire",
    "werewolf",
    "space",
    "anime",
    "kung fu",
    "cartoon",
    "supernatural",
    "education",
    "motivation",
    "comedy-drama",
]

movies = []

for term in search_terms:

    print(f"Searching: {term}")

    for page in range(1, 11):

        url = (
            f"http://www.omdbapi.com/"
            f"?apikey={API_KEY}"
            f"&s={term}"
            f"&page={page}"
        )

        response = requests.get(url)

        data = response.json()

        if data.get("Response") == "True":

            movies.extend(data["Search"])

        time.sleep(0.2)

df = pd.DataFrame(movies)

print("Before Dedup:", len(df))

df.drop_duplicates(
    subset=["imdbID"],
    inplace=True
)

print("After Dedup:", len(df))

os.makedirs(
    "data",
    exist_ok=True
)

df.to_csv(
    "data/raw_movies2.csv",
    index=False
)

print("raw_movies2.csv saved")