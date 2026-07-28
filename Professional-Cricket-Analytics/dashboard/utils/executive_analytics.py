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

SEASON_COLUMNS = [
    "season",
    "Season",
]

DELIVERY_MATCH_ID_COLUMNS = [
    "match_id",
    "id",
    "Match_ID",
    "MatchId",
]
RESULT_COLUMNS = [
    "result",
    "match_result",
]
TOSS_WINNER_COLUMNS = [
    "toss_winner",
    "tossWinner",
]

TOSS_DECISION_COLUMNS = [
    "toss_decision",
    "tossDecision",
]

WIN_BY_RUNS_COLUMNS = [
    "win_by_runs",
    "result_margin_runs",
]

WIN_BY_WICKETS_COLUMNS = [
    "win_by_wickets",
    "result_margin_wickets",
]

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

# ==========================================================
# Season-level trend preparation
# ==========================================================

def create_matches_by_season_summary(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a season-level match-count summary.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Filtered match-level data.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Season
        - Matches
    """

    if matches_df.empty:
        return pd.DataFrame(
            columns=[
                "Season",
                "Matches",
            ]
        )

    season_column = find_first_available_column(
        matches_df,
        SEASON_COLUMNS,
    )

    summary_df = (
        matches_df
        .groupby(
            season_column,
            dropna=False,
        )
        .size()
        .reset_index(
            name="Matches"
        )
        .rename(
            columns={
                season_column: "Season",
            }
        )
    )

    summary_df["Matches"] = pd.to_numeric(
        summary_df["Matches"],
        errors="coerce",
    ).fillna(0).astype(int)

    return (
        summary_df
        .sort_values(
            by="Season"
        )
        .reset_index(
            drop=True
        )
    )


def create_runs_by_season_summary(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a season-level total-runs summary.

    Match season information is joined to delivery records
    using the match ID.
    """

    if matches_df.empty or deliveries_df.empty:
        return pd.DataFrame(
            columns=[
                "Season",
                "Runs",
            ]
        )

    match_id_column = find_first_available_column(
        matches_df,
        MATCH_ID_COLUMNS,
    )

    delivery_match_id_column = (
        find_first_available_column(
            deliveries_df,
            DELIVERY_MATCH_ID_COLUMNS,
        )
    )

    season_column = find_first_available_column(
        matches_df,
        SEASON_COLUMNS,
    )

    match_season_df = (
        matches_df[
            [
                match_id_column,
                season_column,
            ]
        ]
        .drop_duplicates(
            subset=[
                match_id_column
            ]
        )
        .rename(
            columns={
                match_id_column: "_match_id",
                season_column: "Season",
            }
        )
    )

    delivery_summary_df = deliveries_df.copy()

    delivery_summary_df = delivery_summary_df.rename(
        columns={
            delivery_match_id_column: "_match_id",
        }
    )

    total_runs_column = get_optional_column(
        dataframe=delivery_summary_df,
        candidate_columns=TOTAL_RUN_COLUMNS,
    )

    if total_runs_column is not None:

        delivery_summary_df["_delivery_runs"] = (
            pd.to_numeric(
                delivery_summary_df[
                    total_runs_column
                ],
                errors="coerce",
            )
            .fillna(0)
        )

    else:

        batter_runs_column = get_optional_column(
            dataframe=delivery_summary_df,
            candidate_columns=BATTER_RUN_COLUMNS,
        )

        extra_runs_column = get_optional_column(
            dataframe=delivery_summary_df,
            candidate_columns=EXTRA_RUN_COLUMNS,
        )

        delivery_summary_df["_delivery_runs"] = 0

        if batter_runs_column is not None:
            delivery_summary_df[
                "_delivery_runs"
            ] += (
                pd.to_numeric(
                    delivery_summary_df[
                        batter_runs_column
                    ],
                    errors="coerce",
                )
                .fillna(0)
            )

        if extra_runs_column is not None:
            delivery_summary_df[
                "_delivery_runs"
            ] += (
                pd.to_numeric(
                    delivery_summary_df[
                        extra_runs_column
                    ],
                    errors="coerce",
                )
                .fillna(0)
            )

    merged_df = delivery_summary_df.merge(
        match_season_df,
        on="_match_id",
        how="inner",
    )

    if merged_df.empty:
        return pd.DataFrame(
            columns=[
                "Season",
                "Runs",
            ]
        )

    summary_df = (
        merged_df
        .groupby(
            "Season",
            dropna=False,
        )["_delivery_runs"]
        .sum()
        .reset_index(
            name="Runs"
        )
    )

    summary_df["Runs"] = (
        pd.to_numeric(
            summary_df["Runs"],
            errors="coerce",
        )
        .fillna(0)
        .round()
        .astype(int)
    )

    return (
        summary_df
        .sort_values(
            by="Season"
        )
        .reset_index(
            drop=True
        )
    )

# ==========================================================
# Team performance analysis
# ==========================================================

def normalise_text_series(
    series: pd.Series,
) -> pd.Series:
    """
    Convert a Series into clean comparable text values.
    """

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )

def create_team_performance_summary(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate team-level match performance statistics.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Filtered match-level dataset.

    Returns
    -------
    pd.DataFrame
        Team performance summary containing:

        - Team
        - Matches
        - Wins
        - Losses
        - No Results
        - Win Percentage
    """

    output_columns = [
        "Team",
        "Matches",
        "Wins",
        "Losses",
        "No Results",
        "Win Percentage",
    ]

    if matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    team_1_column = find_first_available_column(
        matches_df,
        TEAM_1_COLUMNS,
    )

    team_2_column = find_first_available_column(
        matches_df,
        TEAM_2_COLUMNS,
    )

    winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WINNER_COLUMNS,
    )

    result_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=RESULT_COLUMNS,
    )

    analysis_df = matches_df.copy()

    analysis_df["_team_1"] = normalise_text_series(
        analysis_df[team_1_column]
    )

    analysis_df["_team_2"] = normalise_text_series(
        analysis_df[team_2_column]
    )

    if winner_column is not None:
        analysis_df["_winner"] = normalise_text_series(
            analysis_df[winner_column]
        )
    else:
        analysis_df["_winner"] = ""

    if result_column is not None:
        analysis_df["_result"] = (
            normalise_text_series(
                analysis_df[result_column]
            )
            .str.lower()
        )
    else:
        analysis_df["_result"] = ""

    participating_teams = sorted(
        set(
            analysis_df["_team_1"].tolist()
            +
            analysis_df["_team_2"].tolist()
        )
        - {""}
    )

    performance_records = []

    for team in participating_teams:

        team_matches = analysis_df[
            analysis_df["_team_1"].eq(team)
            |
            analysis_df["_team_2"].eq(team)
        ].copy()

        matches_played = int(
            len(team_matches)
        )

        wins = int(
            team_matches["_winner"]
            .eq(team)
            .sum()
        )

        missing_winner = (
            team_matches["_winner"]
            .eq("")
        )

        if result_column is not None:

            no_result_condition = (
                missing_winner
                |
                team_matches["_result"]
                .isin(
                    [
                        "no result",
                        "abandoned",
                        "cancelled",
                        "canceled",
                    ]
                )
            )

        else:
            no_result_condition = missing_winner

        no_results = int(
            no_result_condition.sum()
        )

        losses = max(
            matches_played
            - wins
            - no_results,
            0,
        )

        decided_matches = (
            matches_played
            - no_results
        )

        win_percentage = (
            safe_divide(
                numerator=wins,
                denominator=decided_matches,
            )
            * 100
        )

        performance_records.append(
            {
                "Team": team,
                "Matches": matches_played,
                "Wins": wins,
                "Losses": losses,
                "No Results": no_results,
                "Win Percentage": round(
                    win_percentage,
                    1,
                ),
            }
        )

    summary_df = pd.DataFrame(
        performance_records,
        columns=output_columns,
    )

    if summary_df.empty:
        return summary_df

    integer_columns = [
        "Matches",
        "Wins",
        "Losses",
        "No Results",
    ]

    for column in integer_columns:
        summary_df[column] = (
            pd.to_numeric(
                summary_df[column],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )

    summary_df["Win Percentage"] = (
        pd.to_numeric(
            summary_df["Win Percentage"],
            errors="coerce",
        )
        .fillna(0)
        .round(1)
    )

    return (
        summary_df
        .sort_values(
            by=[
                "Wins",
                "Win Percentage",
                "Matches",
            ],
            ascending=[
                False,
                False,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )

def create_team_wins_ranking(
    team_summary_df: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Return teams ranked by total match wins.
    """

    required_columns = [
        "Team",
        "Wins",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in team_summary_df.columns
    ]

    if missing_columns:
        raise KeyError(
            "Team summary is missing required columns: "
            f"{missing_columns}"
        )

    if team_summary_df.empty:
        return pd.DataFrame(
            columns=[
                "Team",
                "Wins",
            ]
        )

    return (
        team_summary_df[
            [
                "Team",
                "Wins",
            ]
        ]
        .sort_values(
            by="Wins",
            ascending=False,
        )
        .head(top_n)
        .reset_index(
            drop=True
        )
    )

def create_team_win_percentage_ranking(
    team_summary_df: pd.DataFrame,
    minimum_matches: int = 1,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Rank teams according to win percentage.

    Parameters
    ----------
    team_summary_df : pd.DataFrame
        Team performance summary.

    minimum_matches : int
        Minimum number of matches required for ranking.

    top_n : int
        Maximum number of teams returned.
    """

    required_columns = [
        "Team",
        "Matches",
        "Wins",
        "Win Percentage",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in team_summary_df.columns
    ]

    if missing_columns:
        raise KeyError(
            "Team summary is missing required columns: "
            f"{missing_columns}"
        )

    if team_summary_df.empty:
        return pd.DataFrame(
            columns=[
                "Team",
                "Matches",
                "Win Percentage",
            ]
        )

    qualified_df = team_summary_df[
        team_summary_df["Matches"]
        >= minimum_matches
    ].copy()

    qualified_df = (
        qualified_df
        .sort_values(
            by=[
                "Win Percentage",
                "Wins",
                "Matches",
            ],
            ascending=[
                False,
                False,
                False,
            ],
        )
        .head(top_n)
        .reset_index(
            drop=True
        )
    )

    return qualified_df[
        [
            "Team",
            "Matches",
            "Win Percentage",
        ]
    ]

# ==========================================================
# Toss analysis
# ==========================================================

def normalise_toss_decision(
    value: object,
) -> str:
    """
    Standardise toss-decision values.

    Examples
    --------
    bat, batting -> Bat
    field, bowl, bowling -> Field
    """

    cleaned_value = str(value).strip().lower()

    if cleaned_value in {
        "bat",
        "batting",
    }:
        return "Bat"

    if cleaned_value in {
        "field",
        "fielding",
        "bowl",
        "bowling",
    }:
        return "Field"

    return "Unknown"

def create_toss_decision_summary(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the distribution of toss decisions.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Toss Decision
        - Matches
        - Percentage
    """

    output_columns = [
        "Toss Decision",
        "Matches",
        "Percentage",
    ]

    if matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    toss_decision_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=TOSS_DECISION_COLUMNS,
    )

    if toss_decision_column is None:
        return pd.DataFrame(
            columns=output_columns
        )

    analysis_df = matches_df.copy()

    analysis_df["Toss Decision"] = (
        analysis_df[toss_decision_column]
        .apply(normalise_toss_decision)
    )

    analysis_df = analysis_df[
        analysis_df["Toss Decision"]
        .ne("Unknown")
    ]

    if analysis_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    summary_df = (
        analysis_df
        .groupby(
            "Toss Decision",
            dropna=False,
        )
        .size()
        .reset_index(
            name="Matches"
        )
    )

    total_matches = int(
        summary_df["Matches"].sum()
    )

    summary_df["Percentage"] = (
        summary_df["Matches"]
        .apply(
            lambda value: (
                safe_divide(
                    numerator=value,
                    denominator=total_matches,
                )
                * 100
            )
        )
        .round(1)
    )

    decision_order = {
        "Bat": 1,
        "Field": 2,
    }

    summary_df["_decision_order"] = (
        summary_df["Toss Decision"]
        .map(decision_order)
        .fillna(99)
    )

    return (
        summary_df
        .sort_values(
            by="_decision_order"
        )
        .drop(
            columns="_decision_order"
        )
        .reset_index(
            drop=True
        )
    )

def create_toss_impact_summary(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Analyse whether the toss-winning team also won the match.

    No-result matches are excluded from the percentage denominator.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Outcome
        - Matches
        - Percentage
    """

    output_columns = [
        "Outcome",
        "Matches",
        "Percentage",
    ]

    if matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    toss_winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=TOSS_WINNER_COLUMNS,
    )

    winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WINNER_COLUMNS,
    )

    if (
        toss_winner_column is None
        or winner_column is None
    ):
        return pd.DataFrame(
            columns=output_columns
        )

    analysis_df = matches_df.copy()

    analysis_df["_toss_winner"] = (
        normalise_text_series(
            analysis_df[toss_winner_column]
        )
    )

    analysis_df["_match_winner"] = (
        normalise_text_series(
            analysis_df[winner_column]
        )
    )

    decided_matches_df = analysis_df[
        analysis_df["_match_winner"].ne("")
        & analysis_df["_toss_winner"].ne("")
    ].copy()

    if decided_matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    toss_winner_won = int(
        decided_matches_df[
            "_toss_winner"
        ]
        .eq(
            decided_matches_df[
                "_match_winner"
            ]
        )
        .sum()
    )

    toss_winner_lost = int(
        len(decided_matches_df)
        - toss_winner_won
    )

    total_decided_matches = int(
        len(decided_matches_df)
    )

    summary_df = pd.DataFrame(
        [
            {
                "Outcome": "Toss Winner Won Match",
                "Matches": toss_winner_won,
                "Percentage": round(
                    safe_divide(
                        numerator=toss_winner_won,
                        denominator=total_decided_matches,
                    )
                    * 100,
                    1,
                ),
            },
            {
                "Outcome": "Toss Winner Lost Match",
                "Matches": toss_winner_lost,
                "Percentage": round(
                    safe_divide(
                        numerator=toss_winner_lost,
                        denominator=total_decided_matches,
                    )
                    * 100,
                    1,
                ),
            },
        ],
        columns=output_columns,
    )

    return summary_df

# ==========================================================
# Innings-result analysis
# ==========================================================

def classify_match_outcome_type(
    row: pd.Series,
    win_by_runs_column: str | None,
    win_by_wickets_column: str | None,
) -> str:
    """
    Classify a match as:

    - Batting First Win
    - Chasing Win
    - No Result / Unknown
    """

    if win_by_runs_column is not None:

        win_by_runs = pd.to_numeric(
            row.get(
                win_by_runs_column,
                0,
            ),
            errors="coerce",
        )

        if pd.notna(win_by_runs) and win_by_runs > 0:
            return "Batting First Win"

    if win_by_wickets_column is not None:

        win_by_wickets = pd.to_numeric(
            row.get(
                win_by_wickets_column,
                0,
            ),
            errors="coerce",
        )

        if (
            pd.notna(win_by_wickets)
            and win_by_wickets > 0
        ):
            return "Chasing Win"

    return "No Result / Unknown"

def create_innings_outcome_summary(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare batting-first wins with chasing wins.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Match Outcome
        - Matches
        - Percentage
    """

    output_columns = [
        "Match Outcome",
        "Matches",
        "Percentage",
    ]

    if matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    win_by_runs_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WIN_BY_RUNS_COLUMNS,
    )

    win_by_wickets_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WIN_BY_WICKETS_COLUMNS,
    )

    if (
        win_by_runs_column is None
        and win_by_wickets_column is None
    ):
        return pd.DataFrame(
            columns=output_columns
        )

    analysis_df = matches_df.copy()

    analysis_df["Match Outcome"] = (
        analysis_df.apply(
            classify_match_outcome_type,
            axis=1,
            win_by_runs_column=win_by_runs_column,
            win_by_wickets_column=win_by_wickets_column,
        )
    )

    decided_matches_df = analysis_df[
        analysis_df["Match Outcome"]
        .isin(
            [
                "Batting First Win",
                "Chasing Win",
            ]
        )
    ].copy()

    if decided_matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    summary_df = (
        decided_matches_df
        .groupby(
            "Match Outcome",
            dropna=False,
        )
        .size()
        .reset_index(
            name="Matches"
        )
    )

    total_decided_matches = int(
        summary_df["Matches"].sum()
    )

    summary_df["Percentage"] = (
        summary_df["Matches"]
        .apply(
            lambda value: (
                safe_divide(
                    numerator=value,
                    denominator=total_decided_matches,
                )
                * 100
            )
        )
        .round(1)
    )

    outcome_order = {
        "Batting First Win": 1,
        "Chasing Win": 2,
    }

    summary_df["_outcome_order"] = (
        summary_df["Match Outcome"]
        .map(outcome_order)
        .fillna(99)
    )

    return (
        summary_df
        .sort_values(
            by="_outcome_order"
        )
        .drop(
            columns="_outcome_order"
        )
        .reset_index(
            drop=True
        )
    )

def create_innings_outcome_by_season(
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate batting-first and chasing wins by season.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Season
        - Match Outcome
        - Matches
    """

    output_columns = [
        "Season",
        "Match Outcome",
        "Matches",
    ]

    if matches_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    season_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=SEASON_COLUMNS,
    )

    win_by_runs_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WIN_BY_RUNS_COLUMNS,
    )

    win_by_wickets_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WIN_BY_WICKETS_COLUMNS,
    )

    if (
        season_column is None
        or (
            win_by_runs_column is None
            and win_by_wickets_column is None
        )
    ):
        return pd.DataFrame(
            columns=output_columns
        )

    analysis_df = matches_df.copy()

    analysis_df["Match Outcome"] = (
        analysis_df.apply(
            classify_match_outcome_type,
            axis=1,
            win_by_runs_column=win_by_runs_column,
            win_by_wickets_column=win_by_wickets_column,
        )
    )

    analysis_df = analysis_df[
        analysis_df["Match Outcome"]
        .isin(
            [
                "Batting First Win",
                "Chasing Win",
            ]
        )
    ].copy()

    if analysis_df.empty:
        return pd.DataFrame(
            columns=output_columns
        )

    summary_df = (
        analysis_df
        .groupby(
            [
                season_column,
                "Match Outcome",
            ],
            dropna=False,
        )
        .size()
        .reset_index(
            name="Matches"
        )
        .rename(
            columns={
                season_column: "Season",
            }
        )
    )

    summary_df["Matches"] = (
        pd.to_numeric(
            summary_df["Matches"],
            errors="coerce",
        )
        .fillna(0)
        .astype(int)
    )

    return (
        summary_df
        .sort_values(
            by=[
                "Season",
                "Match Outcome",
            ]
        )
        .reset_index(
            drop=True
        )
    )

