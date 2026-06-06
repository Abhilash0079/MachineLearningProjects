import pandas as pd

raw_df = pd.read_csv("data/raw_movies2.csv")
enriched_df = pd.read_csv("data/movies_data2.csv")

missing_ids = set(raw_df["imdbID"]) - set(enriched_df["imdbID"])

missing_df = pd.DataFrame({"imdbID": list(missing_ids)})

print(f"Missing IMDb IDs: {len(missing_df)}")

missing_df.to_csv("data/missing_ids2.csv", index=False)