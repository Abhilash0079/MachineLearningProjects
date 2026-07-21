import logging
from datetime import datetime
from pathlib import Path


LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

log_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log")
log_file_path = LOG_DIRECTORY / log_file_name

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("loan_default_project")