import os
import logging
import requests
import pandas as pd
from io import StringIO
from datetime import datetime

# ======================================================
# CONFIGURATION
# ======================================================

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "owid/covid-19-data/master/public/data/"
    "owid-covid-data.csv"
)

RAW_DATA_DIR = "data/raw"
LOG_DIR = "logs"

FILE_NAME = "covid_data.csv"

# ======================================================
# CREATE REQUIRED FOLDERS
# ======================================================

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ======================================================
# LOGGING CONFIGURATION
# ======================================================

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ======================================================
# DOWNLOAD DATASET
# ======================================================

def download_dataset():
    """
    Downloads latest COVID dataset from OWID GitHub.
    """

    try:
        logging.info("Starting dataset download")

        response = requests.get(
            DATA_URL,
            timeout=120
        )

        response.raise_for_status()

        df = pd.read_csv(
            StringIO(response.text)
        )

        logging.info(
            "Dataset downloaded successfully"
        )

        return df

    except requests.exceptions.RequestException as e:

        logging.error(
            f"Download failed: {e}"
        )

        raise


# ======================================================
# VALIDATE DATASET
# ======================================================

def validate_dataset(df):
    """
    Performs basic data validation.
    """

    logging.info("Validation started")

    if df.empty:
        raise ValueError(
            "Dataset is empty."
        )

    if df.shape[0] < 1000:
        raise ValueError(
            "Dataset seems incomplete."
        )

    required_columns = [
        "location",
        "date",
        "total_cases",
        "new_cases"
    ]

    missing_cols = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Missing columns: {missing_cols}"
        )

    logging.info(
        f"Rows: {df.shape[0]}"
    )

    logging.info(
        f"Columns: {df.shape[1]}"
    )

    logging.info(
        "Validation completed"
    )


# ======================================================
# SAVE DATASET
# ======================================================

def save_dataset(df):

    filepath = os.path.join(
        RAW_DATA_DIR,
        FILE_NAME
    )

    df.to_csv(
        filepath,
        index=False
    )

    logging.info(
        f"Dataset saved to {filepath}"
    )

    return filepath


# ======================================================
# DATA SUMMARY
# ======================================================

def dataset_summary(df):

    print("\n========== DATASET SUMMARY ==========")

    print(
        f"Rows       : {df.shape[0]:,}"
    )

    print(
        f"Columns    : {df.shape[1]}"
    )

    print(
        f"Memory(MB) : "
        f"{df.memory_usage(deep=True).sum()/1024**2:.2f}"
    )

    print(
        f"Countries  : "
        f"{df['location'].nunique():,}"
    )

    print(
        f"Date Range : "
        f"{df['date'].min()} "
        f"to "
        f"{df['date'].max()}"
    )

    print("=====================================\n")


# ======================================================
# MAIN
# ======================================================

def main():

    print("\nDownloading dataset...")

    df = download_dataset()

    print("Validating dataset...")

    validate_dataset(df)

    print("Saving dataset...")

    filepath = save_dataset(df)

    dataset_summary(df)

    print("SUCCESS")
    print(f"Dataset saved at: {filepath}")

    logging.info(
        "Ingestion pipeline completed successfully"
    )


if __name__ == "__main__":
    main()