#===================================
# STEP 1: DATA LOADING CHECK
#===================================
import pandas as pd

df = pd.read_csv("data/raw/customer_churn.csv")

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample:")
print(df.head())