from pathlib import Path
from typing import Dict
import pandas as pd
import streamlit as st
from config import PROCESSED_DATA_DIR

# ==========================================================
# Dataset filenames
# ==========================================================
MATCHES_FILE = PROCESSED_DATA_DIR / "matches.csv"
DELIVERIES_FILE = PROCESSED_DATA_DIR / "deliveries.csv"
PLAYERS_FILE = PROCESSED_DATA_DIR / "players.csv"

# ==========================================================
# File validation
# ==========================================================
def validate_data_file(file_path:Path)-> None:
    """
    Validate that a dataset exists and is not empty.

    Parameters
    ----------
    file_path : Path
        Path of the CSV file to validate.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    ValueError
        If the file exists but is empty.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if file_path.stat().st_size==0:
        raise ValueError(f"Dataset is empty: {file_path}")

# ==========================================================
# Cached CSV reader
# ==========================================================
@st.cache_data(show_spinner=False)
def read_csv_file(file_path: str, modified_time: float) -> pd.DataFrame:
    """
    Read and cache a CSV file.

    The modified_time argument ensures that Streamlit reloads
    the dataset whenever the source CSV file changes.

    Parameters
    ----------
    file_path : str
        Full path of the CSV file.

    modified_time : float
        Last modification timestamp of the file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """

    del modified_time

    return pd.read_csv(
        file_path,
        low_memory=False
    )

# ==========================================================
# Generic dataset loader
# ==========================================================
def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Validate and load a processed CSV dataset.

    Parameters
    ----------
    file_path : Path
        Path of the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """

    validate_data_file(file_path)
    modified_time = file_path.stat().st_mtime
    dataframe = read_csv_file(
        file_path=str(file_path),
        modified_time=modified_time
    )

    if dataframe.empty:
        raise ValueError(
            f"The loaded dataset contains no rows: {file_path.name}"
        )

    return dataframe

# ==========================================================
# Individual dataset loaders
# ==========================================================
def load_matches_data() -> pd.DataFrame:
    """
    Load the processed match-level dataset.
    """
    return load_dataset(MATCHES_FILE)


def load_deliveries_data() -> pd.DataFrame:
    """
    Load the processed ball-by-ball delivery dataset.
    """
    return load_dataset(DELIVERIES_FILE)


def load_players_data() -> pd.DataFrame:
    """
    Load the processed player registry dataset.
    """
    return load_dataset(PLAYERS_FILE)

# ==========================================================
# Combined data loader
# ==========================================================
def load_all_data() -> Dict[str, pd.DataFrame]:
    """
    Load all datasets required by the dashboard.

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary containing matches, deliveries and players.
    """

    return {
        "matches": load_matches_data(),
        "deliveries": load_deliveries_data(),
        "players": load_players_data()
    }