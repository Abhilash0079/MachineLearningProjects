import pandas as pd

def load_india_data():
    df = pd.read_csv("data/processed/india_ml_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df