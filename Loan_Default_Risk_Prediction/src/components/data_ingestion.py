from pathlib import Path

import pandas as pd

from src.logger import logger
from src.utils.common import read_yaml


class DataIngestion:
    """
    Reads the raw dataset from the configured location.
    """

    def __init__(self):

        config = read_yaml("config/config.yaml")

        self.raw_data_path = config["data"]["raw_data_path"]

    def load_data(self) -> pd.DataFrame:

        logger.info("Loading dataset...")

        dataframe = pd.read_csv(self.raw_data_path)

        logger.info("Dataset loaded successfully.")

        return dataframe