import pandas as pd

df = pd.read_csv(
    "data/processed/covid_ml_dataset.csv"
)

last_date = df["date"].max()