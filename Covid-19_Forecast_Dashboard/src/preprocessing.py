import pandas as pd
import numpy as np
import os

INPUT_FILE = "data/raw/covid_data.csv"

OUTPUT_FILE = (
    "data/processed/covid_ML_dataset.csv"
)

os.makedirs(
    "data/processed",
    exist_ok=True
)

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original Shape:", df.shape)

# -----------------------------------
# Required Columns
# -----------------------------------

required_cols = [

    "iso_code",
    "continent",
    "location",
    "date",

    "total_cases",
    "new_cases",

    "total_deaths",
    "new_deaths",

    "people_vaccinated",

    "population"
]

df = df[required_cols]

# -----------------------------------
# Date
# -----------------------------------

df["date"] = pd.to_datetime(
    df["date"]
)

# -----------------------------------
# Missing Values
# -----------------------------------

numeric_cols = [

    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
    "people_vaccinated",
    "population"
]

df[numeric_cols] = (
    df[numeric_cols]
    .fillna(0)
)

# -----------------------------------
# Sort
# -----------------------------------

df = df.sort_values(
    ["location", "date"]
)

# -----------------------------------
# Feature Engineering
# -----------------------------------

df["mortality_rate"] = np.where(
    df["total_cases"] > 0,
    (
        df["total_deaths"]
        / df["total_cases"]
    ) * 100,
    0
)

df["vaccination_rate"] = np.where(
    df["population"] > 0,
    (
        df["people_vaccinated"]
        / df["population"]
    ) * 100,
    0
)

# -----------------------------------
# Rolling Features
# -----------------------------------

df["cases_7d_avg"] = (

    df.groupby("location")
      ["new_cases"]

      .transform(
          lambda x:
          x.rolling(
              7,
              min_periods=1
          ).mean()
      )
)

df["cases_14d_avg"] = (

    df.groupby("location")
      ["new_cases"]

      .transform(
          lambda x:
          x.rolling(
              14,
              min_periods=1
          ).mean()
      )
)

# -----------------------------------
# Time Features
# -----------------------------------

df["year"] = df["date"].dt.year

df["month"] = df["date"].dt.month

df["day"] = df["date"].dt.day

df["weekday"] = (
    df["date"]
      .dt.dayofweek
)

# -----------------------------------
# Remove Aggregated Regions
# -----------------------------------

df = df[
    df["continent"].notna()
]

# -----------------------------------
# Save
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Processed Shape:",
    df.shape
)

print(
    f"Saved to: {OUTPUT_FILE}"
)
