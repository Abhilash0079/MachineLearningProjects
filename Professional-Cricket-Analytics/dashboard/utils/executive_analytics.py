from typing import Any

import pandas as pd

from utils.filters import (
    find_first_available_column,
    get_filtered_match_ids,
)
from utils.helpers import safe_divide


# ==========================================================
# Column candidates
# ==========================================================

MATCH_ID_COLUMNS = [
    "match_id",
    "id",
]

TEAM_1_COLUMNS = [
    "team1",
    "team_1",
]

TEAM_2_COLUMNS = [
    "team2",
    "team_2",
]

WINNER_COLUMNS = [
    "winner",
    "winning_team",
]

TOTAL_RUN_COLUMNS = [
    "total_runs",
    "runs_total",
]

BATTER_RUN_COLUMNS = [
    "batter_runs",
    "batsman_runs",
]

EXTRA_RUN_COLUMNS = [
    "extra_runs",
    "extras",
]

IS_WICKET_COLUMNS = [
    "is_wicket",
    "wicket",
]

DISMISSED_PLAYER_COLUMNS = [
    "player_dismissed",
    "dismissed_player",
]

DISMISSAL_KIND_COLUMNS = [
    "dismissal_kind",
    "wicket_type",
]


NON_BOWLER_WICKET_TYPES = {
    "retired hurt",
    "retired out",
    "obstructing the field",
}


# ==========================================================
# Internal helpers
# ==========================================================

def get_optional_column(
    dataframe: pd.DataFrame,
    candidate_columns: list[str],
) -> str | None:
    """
    Return the first available column or None.

    Unlike find_first_available_column(), this helper does not
    raise an exception when none of the candidate columns exist.
    """

    for column in candidate_columns:
        if column in dataframe.columns:
            return column

    return None


def calculate_total_runs(
    deliveries_df: pd.DataFrame,
) -> int:
    """
    Calculate total runs from the filtered deliveries.

    The function first looks for a total-runs column. If it is
    unavailable, it combines batter runs and extra runs.
    """

    if deliveries_df.empty:
        return 0

    total_runs_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=TOTAL_RUN_COLUMNS,
    )

    if total_runs_column is not None:
        return int(
            pd.to_numeric(
                deliveries_df[total_runs_column],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    batter_runs_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=BATTER_RUN_COLUMNS,
    )

    extra_runs_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=EXTRA_RUN_COLUMNS,
    )

    batter_runs = 0
    extra_runs = 0

    if batter_runs_column is not None:
        batter_runs = (
            pd.to_numeric(
                deliveries_df[batter_runs_column],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    if extra_runs_column is not None:
        extra_runs = (
            pd.to_numeric(
                deliveries_df[extra_runs_column],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    return int(
        batter_runs + extra_runs
    )


def calculate_total_wickets(
    deliveries_df: pd.DataFrame,
) -> int:
    """
    Calculate total dismissals from the filtered deliveries.

    Retired hurt, retired out and obstructing the field are excluded
    when dismissal-type information is available.
    """

    if deliveries_df.empty:
        return 0

    dismissed_player_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=DISMISSED_PLAYER_COLUMNS,
    )

    dismissal_kind_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=DISMISSAL_KIND_COLUMNS,
    )

    if dismissed_player_column is not None:

        wicket_rows = deliveries_df[
            deliveries_df[dismissed_player_column].notna()
        ].copy()

        if dismissal_kind_column is not None:

            dismissal_types = (
                wicket_rows[dismissal_kind_column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            wicket_rows = wicket_rows[
                ~dismissal_types.isin(
                    NON_BOWLER_WICKET_TYPES
                )
            ]

        return int(
            len(wicket_rows)
        )

    is_wicket_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=IS_WICKET_COLUMNS,
    )

    if is_wicket_column is not None:
        return int(
            pd.to_numeric(
                deliveries_df[is_wicket_column],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    return 0


def calculate_participating_teams(
    matches_df: pd.DataFrame,
) -> int:
    """
    Count the number of unique teams in filtered matches.
    """

    if matches_df.empty:
        return 0

    team_1_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=TEAM_1_COLUMNS,
    )

    team_2_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=TEAM_2_COLUMNS,
    )

    team_values: list[Any] = []

    if team_1_column is not None:
        team_values.extend(
            matches_df[team_1_column]
            .dropna()
            .tolist()
        )

    if team_2_column is not None:
        team_values.extend(
            matches_df[team_2_column]
            .dropna()
            .tolist()
        )

    cleaned_teams = {
        str(team).strip()
        for team in team_values
        if str(team).strip()
    }

    return len(cleaned_teams)


def calculate_completed_matches(
    matches_df: pd.DataFrame,
) -> int:
    """
    Count matches with a recorded winner.

    If no winner column is available, the filtered match-row count
    is returned.
    """

    if matches_df.empty:
        return 0

    winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WINNER_COLUMNS,
    )

    if winner_column is None:
        return int(
            len(matches_df)
        )

    return int(
        matches_df[winner_column]
        .notna()
        .sum()
    )


# ==========================================================
# Executive KPI summary
# ==========================================================

def calculate_executive_kpis(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> dict[str, int | float]:
    """
    Calculate the main Executive Dashboard KPIs.
    """

    total_matches = int(
        len(matches_df)
    )

    total_runs = calculate_total_runs(
        deliveries_df
    )

    total_wickets = calculate_total_wickets(
        deliveries_df
    )

    participating_teams = calculate_participating_teams(
        matches_df
    )

    completed_matches = calculate_completed_matches(
        matches_df
    )

    average_runs_per_match = safe_divide(
        numerator=total_runs,
        denominator=total_matches,
    )

    average_wickets_per_match = safe_divide(
        numerator=total_wickets,
        denominator=total_matches,
    )

    return {
        "total_matches": total_matches,
        "completed_matches": completed_matches,
        "total_runs": total_runs,
        "total_wickets": total_wickets,
        "participating_teams": participating_teams,
        "average_runs_per_match": average_runs_per_match,
        "average_wickets_per_match": average_wickets_per_match,
    }


# ==========================================================
# Filter delivery records using filtered matches
# ==========================================================

def restrict_deliveries_to_matches(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Restrict deliveries to match IDs contained in matches_df.
    """

    if matches_df.empty or deliveries_df.empty:
        return deliveries_df.iloc[0:0].copy()

    match_ids = get_filtered_match_ids(
        matches_df
    )

    delivery_match_id_column = (
        find_first_available_column(
            deliveries_df,
            MATCH_ID_COLUMNS,
        )
    )

    return (
        deliveries_df[
            deliveries_df[
                delivery_match_id_column
            ].isin(match_ids)
        ]
        .copy()
    )