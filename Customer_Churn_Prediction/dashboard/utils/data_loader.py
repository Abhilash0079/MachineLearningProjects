import pandas as pd

#==================================
# lOAD FEATURED DATASET
#==================================

def load_data():
    df = pd.read_csv("data/processed/churn_featured.csv")

    return df
