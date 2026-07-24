from pathlib import Path


# Root folder of the complete project
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Data folders
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
IPL_RAW_DATA_DIR = RAW_DATA_DIR / "ipl"

PROCESSED_DATA_DIR = DATA_DIR / "processed"


# Processed dataset paths
MATCHES_FILE = PROCESSED_DATA_DIR / "matches.csv"
DELIVERIES_FILE = PROCESSED_DATA_DIR / "deliveries.csv"
PLAYERS_FILE = PROCESSED_DATA_DIR / "players.csv"