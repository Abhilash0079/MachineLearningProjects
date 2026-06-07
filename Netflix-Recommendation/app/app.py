# 1. Import the Libraries
import streamlit as st
import pandas as pd
import pickle
from pathlib import Path

# 2. Define Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

# 3. Load the saved file
movies = pd.read_pickle(
    MODELS_DIR / "movies_improved.pkl"
)

with open(MODELS_DIR / "cosine_similarity_improved.pkl","rb") as f:
    cosine_sim = pickle.load(f)

# 4. Create Recommend Function
def recommend(movie_title, top_n=10):

    matches = movies[movies["Title"].str.lower()==movie_title.lower()]

    if len(matches) == 0:
        return None

    idx = matches.index[0]

    scores = []

    for i, similarity in enumerate(cosine_sim[idx]):

        rating = movies.iloc[i]["rating_norm"]

        final_score = (0.85 * similarity + 0.15 * rating)

        scores.append((i, final_score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:top_n+1]

    movie_ids = [i[0] for i in scores]

    return movies.iloc[movie_ids][["Title", "imdbRating"]]

# 5. Configure Stramlit Page
st.set_page_config(
    page_title="Netflix Recommendation System",
    page_icon="🎬",
    layout="wide"
)

#  5.1 Create Header
st.title(
    "🎬 Netflix Recommendation System"
)

st.markdown(
    """
    Recommend movies using
    Content-Based Filtering,
    TF-IDF and Cosine Similarity.
    """
)

# 5.2 Create Movie Dropdown
movie_list = sorted(
    movies["Title"].unique()
)

selected_movie = st.selectbox(
    "Choose a Movie",
    movie_list
)

# 5.3 Create Button
if st.button("Recommend Movies"):
    recommendations = recommend(selected_movie)

    if recommendations is not None:

        st.subheader("Top Recommendations")

        st.dataframe(
            recommendations,
            use_container_width=True
        )

    else:
        st.error("Movie not found.")
