import pandas as pd

FILE_PATH = "data/raw/spam_emails.csv"

df = pd.read_csv(FILE_PATH)

print(df.head())
print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTarget Distribution:")
print(df.iloc[:, -1].value_counts())