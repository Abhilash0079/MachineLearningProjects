import pandas as pd

def load_data():
    df = pd.read_csv("data/processed/spam_featured.csv")
    return df
