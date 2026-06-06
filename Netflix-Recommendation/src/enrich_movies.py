import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

# Load API KEY
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OMDB_API_KEY")

# Load raw_movies
# raw_df = pd.read_csv("data/raw_movies2.csv")

# Missing IDs
missing_df= pd.read_csv("data/missing_ids2.csv")


movie_details = []

for imdb_id in tqdm(missing_df["imdbID"]):
    url = (
        f"http://www.omdbapi.com/"
        f"?apikey={API_KEY}"
        f"&i={imdb_id}"
        f"&plot=full"
    )

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        if data.get("Response") == "True":
            movie_details.append({
                "imdbID": data.get("imdbID"),
                "Title": data.get("Title"),
                "Year": data.get("Year"),
                "Type": data.get("Type"),
                "Genre": data.get("Genre"),
                "Director": data.get("Director"),
                "Writer": data.get("Writer"),
                "Actors": data.get("Actors"),
                "Plot": data.get("Plot"),
                "Language": data.get("Language"),
                "Country": data.get("Country"),
                "Runtime": data.get("Runtime"),
                "Rated": data.get("Rated"),
                "Awards": data.get("Awards"),
                "imdbRating": data.get("imdbRating"),
                "imdbVotes": data.get("imdbVotes"),
                "Poster": data.get("Poster")
            })
        time.sleep(0.1)
    except Exception as e:
        print(e)

# enriched_df = pd.DataFrame(movie_details)
# print(f"Rows Collected: {len(enriched_df)}")

# enriched_df.to_csv(
#     "data/movies_data2.csv",
#     index=False
# )

# print("movies_data2.csv saved successfully!")

'''
More Missing IDs
'''

new_df = pd.DataFrame(movie_details)

new_df.to_csv(
    "data/movies_enriched_part3.csv",
    index=False
)

print("Rows Collected:", len(new_df))
    