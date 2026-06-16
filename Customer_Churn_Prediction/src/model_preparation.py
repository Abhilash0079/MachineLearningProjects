#==========================
# 5. MODEL PREPARATION
#==========================

import pandas as pd
import os

#===========================
# LOAD DATA
#===========================
INPUT_FILE = "data/processed/churn_featured.csv"
OUTPUT_FILE = "data/processed/churn_model_data.csv"

df = pd.read_csv(INPUT_FILE)
print(f"Original Shape: {df.shape}")

#===========================
# BINARY ENCODING
#===========================
binary_cols = [
    'Partner',
    'Dependents',
    'PhoneService',
    'PaperlessBilling'
]

for col in binary_cols:
    df[col] = df[col].map({
        "No":0,
        "Yes":1
    })

#===========================
# ONE HOT ENCODING
#===========================
categorical_cols = [
    'gender',
    'MultipleLines',
    'InternetService',
    'OnlineSecurity',
    'OnlineBackup',
    'DeviceProtection',
    'TechSupport',
    'StreamingTV',
    'StreamingMovies',
    'Contract',
    'PaymentMethod',
    'TenureGroup'
]

df = pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=True
)

#=======================
# SAVE
#=======================
df.to_csv(
    OUTPUT_FILE,
    index=False
)
print(f"Processed Shape: {df.shape}")
print(f"Saved to : {OUTPUT_FILE}")