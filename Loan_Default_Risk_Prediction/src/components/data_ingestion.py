import pandas as pd
from pathlib import Path
from src.logger import logger
from src.utils.common import read_yaml


class DataIngestion:
    """
    Reads the raw dataset from the configured location.
    """

    def __init__(self):
        # Project root
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config" / "config.yaml"
        config = read_yaml(config_path)
        self.raw_data_path = (
            project_root / config["data"]["raw_data_path"]
        )

    def load_data(self) -> pd.DataFrame:
        logger.info("Loading dataset from: %s", self.raw_data_path)
        if not self.raw_data_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at: {self.raw_data_path}"
            )
        dataframe = pd.read_csv(self.raw_data_path)
        logger.info(
            "Dataset loaded successfully with shape: %s",
            dataframe.shape,
        )

        return dataframe