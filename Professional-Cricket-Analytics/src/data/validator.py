from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_TOP_LEVEL_KEYS = {
    "meta",
    "info",
    "innings",
}


def validate_match_json(
    match_data: dict[str, Any],
    file_path: Path
) -> None:
    """
    Validate the basic structure of one match JSON file.

    Raises
    ------
    ValueError
        If required sections are missing or invalid.
    """

    if not isinstance(match_data, dict):
        raise ValueError(
            f"JSON root must be a dictionary: {file_path.name}"
        )

    missing_keys = REQUIRED_TOP_LEVEL_KEYS.difference(
        match_data.keys()
    )

    if missing_keys:
        raise ValueError(
            f"Missing required keys {missing_keys} "
            f"in file: {file_path.name}"
        )

    if not isinstance(match_data["info"], dict):
        raise ValueError(
            f"'info' must be a dictionary: {file_path.name}"
        )

    if not isinstance(match_data["innings"], list):
        raise ValueError(
            f"'innings' must be a list: {file_path.name}"
        )

    teams = match_data["info"].get("teams", [])

    if len(teams) < 2:
        raise ValueError(
            f"Expected at least two teams: {file_path.name}"
        )


def validate_matches_dataframe(
    matches_df: pd.DataFrame
) -> None:
    """
    Validate the processed match-level DataFrame.
    """

    required_columns = {
        "match_id",
        "season",
        "team_1",
        "team_2",
        "venue",
    }

    missing_columns = required_columns.difference(
        matches_df.columns
    )

    if missing_columns:
        raise ValueError(
            f"Matches DataFrame is missing columns: "
            f"{missing_columns}"
        )

    if matches_df.empty:
        raise ValueError(
            "Matches DataFrame is empty."
        )

    duplicate_match_ids = matches_df[
        "match_id"
    ].duplicated().sum()

    if duplicate_match_ids > 0:
        raise ValueError(
            f"Found {duplicate_match_ids} duplicate match IDs."
        )


def validate_deliveries_dataframe(
    deliveries_df: pd.DataFrame
) -> None:
    """
    Validate the processed delivery-level DataFrame.
    """

    required_columns = {
        "match_id",
        "innings",
        "over",
        "batter",
        "bowler",
        "total_runs",
    }

    missing_columns = required_columns.difference(
        deliveries_df.columns
    )

    if missing_columns:
        raise ValueError(
            f"Deliveries DataFrame is missing columns: "
            f"{missing_columns}"
        )

    if deliveries_df.empty:
        raise ValueError(
            "Deliveries DataFrame is empty."
        )

    invalid_runs = (
        deliveries_df["total_runs"] < 0
    ).sum()

    if invalid_runs > 0:
        raise ValueError(
            f"Found {invalid_runs} deliveries with negative runs."
        )


def validate_players_dataframe(
    players_df: pd.DataFrame
) -> None:
    """
    Validate the player participation DataFrame.
    """

    required_columns = {
        "match_id",
        "team",
        "player_name",
    }

    missing_columns = required_columns.difference(
        players_df.columns
    )

    if missing_columns:
        raise ValueError(
            f"Players DataFrame is missing columns: "
            f"{missing_columns}"
        )

    if players_df.empty:
        raise ValueError(
            "Players DataFrame is empty."
        )