import pandas as pd

from src.config.config import (
    TRAIN_DATA_PATH,
    TEST_DATA_PATH
)


def load_sample_train_data(n_rows=5000):
    """
    Load sample rows from training dataset.
    """
    return pd.read_csv(
        TRAIN_DATA_PATH,
        nrows=n_rows
    )


def load_full_train_data():
    """
    Load complete training dataset.
    """
    return pd.read_csv(
        TRAIN_DATA_PATH
    )


def load_sample_test_data(n_rows=5000):
    """
    Load sample rows from test dataset.
    """
    return pd.read_csv(
        TEST_DATA_PATH,
        nrows=n_rows
    )


def load_full_test_data():
    """
    Load complete test dataset.
    """
    return pd.read_csv(
        TEST_DATA_PATH
    )