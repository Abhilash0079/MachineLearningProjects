import pandas as pd
import os

#===================================================
# CONFIGURATION
#===================================================
COUNTRY="India"

INPUT_FILE = "data\processed\covid_ML_dataset.csv"

OUTPUT_FILE = "data\processed\india_ml_dataset.csv"

#===================================================
# LOAD DATA
#===================================================

print("Loading processed dataset....")

df = pd.read_csv(INPUT_FILE)

print(f"Original Shape: {df.shape}")

#===================================================
# FILTER COUNTRY
#===================================================

india_df = df[df['location']==COUNTRY].copy()

#===================================================
# SORT BY DATE
#===================================================

india_df = india_df.sort_values('date')

#===================================================
# RESET INDEX
#===================================================

india_df.reset_index(drop=True, inplace=True)

#===================================================
# SAVE
#===================================================

india_df.to_csv(OUTPUT_FILE, index=False)

#===================================================
# SUMMARY
#===================================================

print("\nCountry Dataset Created Successfully.")
print(f"Country: {COUNTRY}")
print(f"Shape of Data: {india_df.shape}")
print(f"Date Range: ")
print(india_df['date'].min(), "to", india_df['date'].max())
print(f"\nSaved to : \n{OUTPUT_FILE}")