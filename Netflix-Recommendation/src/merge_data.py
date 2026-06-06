import pandas as pd

df1 = pd.read_csv("data/final_data2.csv")
df2 = pd.read_csv("data/movies_enriched_part3.csv")

final_df = pd.concat([df1, df2], ignore_index=True)

final_df.drop_duplicates(subset="imdbID", inplace=True)

print(final_df.shape)

final_df.to_csv("data/Netflix_data.csv", index=False)