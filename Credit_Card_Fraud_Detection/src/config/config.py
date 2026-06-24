from pathlib import Path

# Project Root Directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Paths
TRAIN_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "fraudTrain.csv"
TEST_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "fraudTest.csv"

# Sample Size
SAMPLE_ROWS = 5000