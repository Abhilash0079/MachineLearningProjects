import pandas as pd
import os

# def load_data():
#     df = pd.read_csv("data/processed/email_featured.csv")
#     return df


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "email_featured.csv"
)

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df