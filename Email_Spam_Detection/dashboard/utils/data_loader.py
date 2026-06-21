import pandas as pd

def load_data():
    df = pd.read_csv("data/processed/email_featured.csv")
    return df
