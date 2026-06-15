#================================
# STEP 2: DATA PREPROCESSING
#================================

import pandas as pd
import numpy as np
import os

#============================
# PATHS
#============================

INPUT_FILE = "data/raw/customer_churn.csv"
OUTPUT_FILE = "data/processed/churn_processed.csv"

os.makedirs("data/processed", exist_ok=True)

#============================
# LOAD DATA
#============================
print("Loading Dataset.....")
df = pd.read_csv(INPUT_FILE)
print(f"Original Shape: {df.shape}")

#============================
# REMOVE CUSTOMER ID
#============================
df = df.drop(columns=['customerID'])

#============================
# FIX TOTAL CHARGES
#============================
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

#============================
# HANDLE MISSING VALUES
#============================
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

#============================
# TARGET ENCODING
#============================
df['Churn'] = df['Churn'].map({"No":0, "Yes":1})

#============================
# BASIC CHECKS
#============================
print("\nMissing Values:")
print(df.isnull().sum())
print("\nTarget Distribution:")
print(df['Churn'].value_counts())

#============================
# SAVE
#============================
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nProcessed Shape: {df.shape}")
print(f"\nSaved to : {OUTPUT_FILE}")