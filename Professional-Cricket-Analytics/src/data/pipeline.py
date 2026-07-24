import logging
from pathlib import Path

import pandas as pd

from src.config import (
    IPL_RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MATCHES_FILE,
    DELIVERIES_FILE,
    PLAYERS_FILE,
)

from src.data.parser import load_json_file

from src.data.extractor import (
    extract_match_record,
    extract_delivery_records,
    extract_player_records,
)

from src.data.validator import (
    validate_match_json,
    validate_matches_dataframe,
    validate_deliveries_dataframe,
    validate_players_dataframe,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def get_json_files(
    input_directory: Path
) -> list[Path]:
    """
    Return all JSON files from the input directory.
    """

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Input directory not found: {input_directory}"
        )

    json_files = sorted(
        input_directory.glob("*.json")
    )

    if not json_files:
        raise FileNotFoundError(
            f"No JSON files found in: {input_directory}"
        )

    return json_files


def build_dataframes(
    json_files: list[Path]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse all JSON files and create processed DataFrames.
    """

    match_records = []
    delivery_records = []
    player_records = []

    failed_files = []

    total_files = len(json_files)

    for index, file_path in enumerate(
        json_files,
        start=1
    ):

        try:
            match_data = load_json_file(file_path)

            validate_match_json(
                match_data=match_data,
                file_path=file_path
            )

            match_record = extract_match_record(
                match_data=match_data,
                file_path=file_path
            )

            deliveries = extract_delivery_records(
                match_data=match_data,
                file_path=file_path
            )

            players = extract_player_records(
                match_data=match_data,
                file_path=file_path
            )

            match_records.append(match_record)
            delivery_records.extend(deliveries)
            player_records.extend(players)

        except (
            FileNotFoundError,
            ValueError,
            KeyError,
            TypeError
        ) as error:

            logger.error(
                "Failed to process %s: %s",
                file_path.name,
                error
            )

            failed_files.append(file_path.name)

        if (
            index % 100 == 0
            or index == total_files
        ):
            logger.info(
                "Processed %s/%s files",
                index,
                total_files
            )

    matches_df = pd.DataFrame(match_records)
    deliveries_df = pd.DataFrame(delivery_records)
    players_df = pd.DataFrame(player_records)

    logger.info(
        "Successfully processed: %s files",
        total_files - len(failed_files)
    )

    logger.info(
        "Failed files: %s",
        len(failed_files)
    )

    if failed_files:
        logger.warning(
            "Failed file names: %s",
            failed_files
        )

    return (
        matches_df,
        deliveries_df,
        players_df
    )


def clean_dataframes(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
    players_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Apply basic cleaning and type conversion.
    """

    matches_df = matches_df.copy()
    deliveries_df = deliveries_df.copy()
    players_df = players_df.copy()

    # Convert date columns
    matches_df["match_date"] = pd.to_datetime(
        matches_df["match_date"],
        errors="coerce"
    )

    deliveries_df["match_date"] = pd.to_datetime(
        deliveries_df["match_date"],
        errors="coerce"
    )

    # Convert IDs to strings
    matches_df["match_id"] = (
        matches_df["match_id"].astype(str)
    )

    deliveries_df["match_id"] = (
        deliveries_df["match_id"].astype(str)
    )

    players_df["match_id"] = (
        players_df["match_id"].astype(str)
    )

    # Remove duplicate match-level records
    matches_df = matches_df.drop_duplicates(
        subset=["match_id"]
    )

    # Remove duplicated player participation rows
    players_df = players_df.drop_duplicates(
        subset=[
            "match_id",
            "team",
            "player_name",
        ]
    )

    # Reset indexes
    matches_df = matches_df.reset_index(
        drop=True
    )

    deliveries_df = deliveries_df.reset_index(
        drop=True
    )

    players_df = players_df.reset_index(
        drop=True
    )

    return (
        matches_df,
        deliveries_df,
        players_df
    )


def save_dataframes(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
    players_df: pd.DataFrame
) -> None:
    """
    Save processed DataFrames as CSV files.
    """

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    matches_df.to_csv(
        MATCHES_FILE,
        index=False
    )

    deliveries_df.to_csv(
        DELIVERIES_FILE,
        index=False
    )

    players_df.to_csv(
        PLAYERS_FILE,
        index=False
    )

    logger.info(
        "Saved matches dataset: %s",
        MATCHES_FILE
    )

    logger.info(
        "Saved deliveries dataset: %s",
        DELIVERIES_FILE
    )

    logger.info(
        "Saved players dataset: %s",
        PLAYERS_FILE
    )


def run_pipeline() -> None:
    """
    Run the complete IPL data-processing pipeline.
    """

    logger.info(
        "Starting IPL data pipeline"
    )

    json_files = get_json_files(
        IPL_RAW_DATA_DIR
    )

    logger.info(
        "Found %s JSON files",
        len(json_files)
    )

    (
        matches_df,
        deliveries_df,
        players_df
    ) = build_dataframes(json_files)

    (
        matches_df,
        deliveries_df,
        players_df
    ) = clean_dataframes(
        matches_df=matches_df,
        deliveries_df=deliveries_df,
        players_df=players_df
    )

    validate_matches_dataframe(
        matches_df
    )

    validate_deliveries_dataframe(
        deliveries_df
    )

    validate_players_dataframe(
        players_df
    )

    save_dataframes(
        matches_df=matches_df,
        deliveries_df=deliveries_df,
        players_df=players_df
    )

    logger.info(
        "Matches shape: %s",
        matches_df.shape
    )

    logger.info(
        "Deliveries shape: %s",
        deliveries_df.shape
    )

    logger.info(
        "Players shape: %s",
        players_df.shape
    )

    logger.info(
        "IPL data pipeline completed successfully"
    )


if __name__ == "__main__":
    run_pipeline()