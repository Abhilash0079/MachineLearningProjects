"""
Team-level analytics utilities.

This module contains calculations used by the
Team Dashboard.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


# ==========================================================
# Column candidates
# ==========================================================

MATCH_ID_COLUMNS = [
    "match_id",
    "id",
    "Match_ID",
    "MatchId",
]

DELIVERY_MATCH_ID_COLUMNS = [
    "match_id",
    "id",
    "Match_ID",
    "MatchId",
]

SEASON_COLUMNS = [
    "season",
    "Season",
]

TEAM_1_COLUMNS = [
    "team1",
    "team_1",
    "Team1",
    "home_team",
]

TEAM_2_COLUMNS = [
    "team2",
    "team_2",
    "Team2",
    "away_team",
]

WINNER_COLUMNS = [
    "winner",
    "winning_team",
]

VENUE_COLUMNS = [
    "venue",
    "Venue",
    "ground",
    "stadium",
]

TOSS_WINNER_COLUMNS = [
    "toss_winner",
    "tossWinner",
]

TOSS_DECISION_COLUMNS = [
    "toss_decision",
    "tossDecision",
]

BATTING_TEAM_COLUMNS = [
    "batting_team",
    "battingTeam",
]

BOWLING_TEAM_COLUMNS = [
    "bowling_team",
    "bowlingTeam",
]

TOTAL_RUN_COLUMNS = [
    "total_runs",
    "totalRuns",
]

BATTER_RUN_COLUMNS = [
    "batter_runs",
    "batsman_runs",
    "runs_off_bat",
]

EXTRA_RUN_COLUMNS = [
    "extra_runs",
    "extras",
]

IS_WICKET_COLUMNS = [
    "is_wicket",
    "isWicket",
]

PLAYER_DISMISSED_COLUMNS = [
    "player_dismissed",
    "playerDismissed",
]

DISMISSAL_KIND_COLUMNS = [
    "dismissal_kind",
    "kind",
]


# ==========================================================
# Generic helpers
# ==========================================================

def get_optional_column(
    dataframe: pd.DataFrame,
    candidate_columns: list[str],
) -> str | None:
    """
    Return the first matching column from a list of candidates.

    Matching is first attempted using exact column names,
    followed by case-insensitive matching.
    """

    for column in candidate_columns:

        if column in dataframe.columns:
            return column

    lowercase_mapping = {
        str(column).lower(): column
        for column in dataframe.columns
    }

    for candidate in candidate_columns:

        matched_column = lowercase_mapping.get(
            candidate.lower()
        )

        if matched_column is not None:
            return matched_column

    return None


def require_column(
    dataframe: pd.DataFrame,
    candidate_columns: list[str],
    field_name: str,
) -> str:
    """
    Return a required column or raise a helpful error.
    """

    column = get_optional_column(
        dataframe=dataframe,
        candidate_columns=candidate_columns,
    )

    if column is None:
        raise KeyError(
            f"Unable to find the required {field_name} column. "
            f"Checked: {candidate_columns}"
        )

    return column


def clean_text_series(
    series: pd.Series,
) -> pd.Series:
    """
    Convert values into clean comparable strings.
    """

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


def safe_divide(
    numerator: float | int,
    denominator: float | int,
    default: float = 0.0,
) -> float:
    """
    Safely divide two numeric values.
    """

    if denominator == 0:
        return default

    return numerator / denominator

def sort_season_dataframe(
    dataframe: pd.DataFrame,
    season_column: str = "Season",
) -> pd.DataFrame:
    """
    Sort a dataframe chronologically using the starting
    year found in the season value.

    Examples
    --------
    2008      -> 2008
    2020/21   -> 2020
    2007-08   -> 2007
    Unknown   -> placed at the end
    """

    if dataframe.empty:
        return dataframe.copy()

    if season_column not in dataframe.columns:
        return dataframe.copy()

    output_df = dataframe.copy()

    season_text = (
        output_df[season_column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    output_df["_season_sort"] = pd.to_numeric(
        season_text.str.extract(
            r"(\d{4})",
            expand=False,
        ),
        errors="coerce",
    )

    output_df["_season_sort"] = (
        output_df["_season_sort"]
        .fillna(float("inf"))
    )

    output_df = (
        output_df
        .sort_values(
            by=[
                "_season_sort",
                season_column,
            ],
            ascending=[
                True,
                True,
            ],
        )
        .drop(
            columns="_season_sort",
        )
    )

    return output_df

def create_team_runs_by_season(
    team: str,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate total runs scored by the selected team
    in each season.

    The deliveries dataframe must contain a Season column.
    """

    output_columns = [
        "Season",
        "Runs Scored",
    ]

    if (
        deliveries_df.empty
        or not team
        or "Season" not in deliveries_df.columns
    ):
        return pd.DataFrame(columns=output_columns)

    batting_team_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=BATTING_TEAM_COLUMNS,
    )

    if batting_team_column is None:
        return pd.DataFrame(columns=output_columns)

    analysis_df = deliveries_df.copy()

    batting_team_values = clean_text_series(
        analysis_df[batting_team_column]
    )

    analysis_df = analysis_df[
        batting_team_values.eq(team)
    ].copy()

    if analysis_df.empty:
        return pd.DataFrame(columns=output_columns)

    total_runs_column = get_optional_column(
        dataframe=analysis_df,
        candidate_columns=TOTAL_RUN_COLUMNS,
    )

    if total_runs_column is not None:

        analysis_df["_team_runs"] = (
            pd.to_numeric(
                analysis_df[total_runs_column],
                errors="coerce",
            )
            .fillna(0)
        )

    else:

        batter_runs_column = get_optional_column(
            dataframe=analysis_df,
            candidate_columns=BATTER_RUN_COLUMNS,
        )

        extra_runs_column = get_optional_column(
            dataframe=analysis_df,
            candidate_columns=EXTRA_RUN_COLUMNS,
        )

        analysis_df["_team_runs"] = 0.0

        if batter_runs_column is not None:

            analysis_df["_team_runs"] += (
                pd.to_numeric(
                    analysis_df[batter_runs_column],
                    errors="coerce",
                )
                .fillna(0)
            )

        if extra_runs_column is not None:

            analysis_df["_team_runs"] += (
                pd.to_numeric(
                    analysis_df[extra_runs_column],
                    errors="coerce",
                )
                .fillna(0)
            )

    summary_df = (
        analysis_df
        .groupby(
            "Season",
            dropna=False,
        )["_team_runs"]
        .sum()
        .reset_index(
            name="Runs Scored"
        )
    )

    summary_df["Runs Scored"] = (
        summary_df["Runs Scored"]
        .round()
        .astype(int)
    )

    return (
        sort_season_dataframe(
            dataframe=summary_df[
                output_columns
            ],
            season_column="Season",
        )
        .reset_index(drop=True)
    )

def create_team_wickets_by_season(
    team: str,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate bowler-credit wickets taken by the selected
    team in each season.

    Run outs and other non-bowler dismissals are excluded.
    """

    output_columns = [
        "Season",
        "Wickets Taken",
    ]

    if (
        deliveries_df.empty
        or not team
        or "Season" not in deliveries_df.columns
    ):
        return pd.DataFrame(columns=output_columns)

    bowling_team_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=BOWLING_TEAM_COLUMNS,
    )

    if bowling_team_column is None:
        return pd.DataFrame(columns=output_columns)

    analysis_df = deliveries_df.copy()

    bowling_team_values = clean_text_series(
        analysis_df[bowling_team_column]
    )

    analysis_df = analysis_df[
        bowling_team_values.eq(team)
    ].copy()

    if analysis_df.empty:
        return pd.DataFrame(columns=output_columns)

    dismissal_kind_column = get_optional_column(
        dataframe=analysis_df,
        candidate_columns=DISMISSAL_KIND_COLUMNS,
    )

    if dismissal_kind_column is not None:

        dismissal_values = (
            clean_text_series(
                analysis_df[dismissal_kind_column]
            )
            .str.lower()
        )

        excluded_dismissals = {
            "",
            "run out",
            "retired hurt",
            "retired out",
            "obstructing the field",
        }

        analysis_df["_is_team_wicket"] = (
            ~dismissal_values.isin(
                excluded_dismissals
            )
        ).astype(int)

    else:

        is_wicket_column = get_optional_column(
            dataframe=analysis_df,
            candidate_columns=IS_WICKET_COLUMNS,
        )

        if is_wicket_column is not None:

            analysis_df["_is_team_wicket"] = (
                pd.to_numeric(
                    analysis_df[is_wicket_column],
                    errors="coerce",
                )
                .fillna(0)
                .eq(1)
                .astype(int)
            )

        else:

            player_dismissed_column = get_optional_column(
                dataframe=analysis_df,
                candidate_columns=PLAYER_DISMISSED_COLUMNS,
            )

            if player_dismissed_column is None:
                return pd.DataFrame(columns=output_columns)

            analysis_df["_is_team_wicket"] = (
                clean_text_series(
                    analysis_df[player_dismissed_column]
                )
                .ne("")
                .astype(int)
            )

    summary_df = (
        analysis_df
        .groupby(
            "Season",
            dropna=False,
        )["_is_team_wicket"]
        .sum()
        .reset_index(
            name="Wickets Taken"
        )
    )

    summary_df["Wickets Taken"] = (
        pd.to_numeric(
            summary_df["Wickets Taken"],
            errors="coerce",
        )
        .fillna(0)
        .astype(int)
    )

    return (
        sort_season_dataframe(
            dataframe=summary_df[
                output_columns
            ],
            season_column="Season",
        )
        .reset_index(drop=True)
    )


# ==========================================================
# Team selection
# ==========================================================

def get_team_options(
    matches_df: pd.DataFrame,
) -> list[str]:
    """
    Return a sorted list of participating teams.
    """

    if matches_df.empty:
        return []

    team_1_column = require_column(
        dataframe=matches_df,
        candidate_columns=TEAM_1_COLUMNS,
        field_name="team 1",
    )

    team_2_column = require_column(
        dataframe=matches_df,
        candidate_columns=TEAM_2_COLUMNS,
        field_name="team 2",
    )

    team_1_values = clean_text_series(
        matches_df[team_1_column]
    )

    team_2_values = clean_text_series(
        matches_df[team_2_column]
    )

    teams = set(
        team_1_values.tolist()
        + team_2_values.tolist()
    )

    teams.discard("")

    return sorted(teams)

# ==========================================================
# Team match filtering
# ==========================================================

def filter_matches_for_team(
    matches_df: pd.DataFrame,
    team: str,
    season: Any = "All",
    venue: str = "All",
) -> pd.DataFrame:
    """
    Filter matches involving the selected team.

    Optional season and venue filters are then applied.
    """

    if matches_df.empty:
        return matches_df.copy()

    if not team or team == "All":
        return matches_df.iloc[0:0].copy()

    team_1_column = require_column(
        dataframe=matches_df,
        candidate_columns=TEAM_1_COLUMNS,
        field_name="team 1",
    )

    team_2_column = require_column(
        dataframe=matches_df,
        candidate_columns=TEAM_2_COLUMNS,
        field_name="team 2",
    )

    filtered_df = matches_df.copy()

    team_1_values = clean_text_series(
        filtered_df[team_1_column]
    )

    team_2_values = clean_text_series(
        filtered_df[team_2_column]
    )

    filtered_df = filtered_df[
        team_1_values.eq(team)
        |
        team_2_values.eq(team)
    ].copy()

    if season != "All":

        season_column = get_optional_column(
            dataframe=filtered_df,
            candidate_columns=SEASON_COLUMNS,
        )

        if season_column is not None:

            filtered_df = filtered_df[
                filtered_df[season_column]
                .astype(str)
                .eq(str(season))
            ].copy()

    if venue != "All":

        venue_column = get_optional_column(
            dataframe=filtered_df,
            candidate_columns=VENUE_COLUMNS,
        )

        if venue_column is not None:

            venue_values = clean_text_series(
                filtered_df[venue_column]
            )

            filtered_df = filtered_df[
                venue_values.eq(venue)
            ].copy()

    return filtered_df.reset_index(
        drop=True
    )

def filter_deliveries_for_team_matches(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return all delivery records belonging to the filtered
    team matches.

    This includes deliveries from both teams because the
    Team Dashboard needs complete match context.
    """

    if matches_df.empty or deliveries_df.empty:
        return deliveries_df.iloc[0:0].copy()

    match_id_column = require_column(
        dataframe=matches_df,
        candidate_columns=MATCH_ID_COLUMNS,
        field_name="match ID",
    )

    delivery_match_id_column = require_column(
        dataframe=deliveries_df,
        candidate_columns=DELIVERY_MATCH_ID_COLUMNS,
        field_name="delivery match ID",
    )

    match_ids = (
        matches_df[match_id_column]
        .dropna()
        .unique()
        .tolist()
    )

    filtered_deliveries_df = deliveries_df[
        deliveries_df[delivery_match_id_column]
        .isin(match_ids)
    ].copy()

    return filtered_deliveries_df.reset_index(
        drop=True
    )

# ==========================================================
# Team KPI calculations
# ==========================================================

def calculate_team_kpis(
    team: str,
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> dict[str, int | float]:
    """
    Calculate high-level KPIs for the selected team.

    KPIs:
    - Matches
    - Wins
    - Losses
    - No Results
    - Win Percentage
    - Runs Scored
    - Wickets Taken
    - Toss Wins
    """

    default_kpis = {
        "matches": 0,
        "wins": 0,
        "losses": 0,
        "no_results": 0,
        "win_percentage": 0.0,
        "runs_scored": 0,
        "wickets_taken": 0,
        "toss_wins": 0,
    }

    if matches_df.empty or not team:
        return default_kpis

    winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WINNER_COLUMNS,
    )

    toss_winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=TOSS_WINNER_COLUMNS,
    )

    matches_played = int(
        len(matches_df)
    )

    if winner_column is not None:

        winner_values = clean_text_series(
            matches_df[winner_column]
        )

        wins = int(
            winner_values.eq(team).sum()
        )

        no_results = int(
            winner_values.eq("").sum()
        )

    else:

        wins = 0
        no_results = matches_played

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

    win_percentage = round(
        safe_divide(
            numerator=wins,
            denominator=decided_matches,
        )
        * 100,
        1,
    )

    if toss_winner_column is not None:

        toss_winner_values = clean_text_series(
            matches_df[toss_winner_column]
        )

        toss_wins = int(
            toss_winner_values.eq(team).sum()
        )

    else:

        toss_wins = 0

    runs_scored = calculate_team_runs_scored(
        team=team,
        deliveries_df=deliveries_df,
    )

    wickets_taken = calculate_team_wickets_taken(
        team=team,
        deliveries_df=deliveries_df,
    )

    return {
        "matches": matches_played,
        "wins": wins,
        "losses": losses,
        "no_results": no_results,
        "win_percentage": win_percentage,
        "runs_scored": runs_scored,
        "wickets_taken": wickets_taken,
        "toss_wins": toss_wins,
    }

def calculate_team_runs_scored(
    team: str,
    deliveries_df: pd.DataFrame,
) -> int:
    """
    Calculate total runs scored by the selected team.
    """

    if deliveries_df.empty:
        return 0

    batting_team_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=BATTING_TEAM_COLUMNS,
    )

    if batting_team_column is None:
        return 0

    batting_team_values = clean_text_series(
        deliveries_df[batting_team_column]
    )

    team_deliveries_df = deliveries_df[
        batting_team_values.eq(team)
    ].copy()

    if team_deliveries_df.empty:
        return 0

    total_runs_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=TOTAL_RUN_COLUMNS,
    )

    if total_runs_column is not None:

        total_runs = (
            pd.to_numeric(
                team_deliveries_df[
                    total_runs_column
                ],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

        return int(round(total_runs))

    batter_runs_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=BATTER_RUN_COLUMNS,
    )

    extra_runs_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=EXTRA_RUN_COLUMNS,
    )

    total_runs = 0.0

    if batter_runs_column is not None:

        total_runs += (
            pd.to_numeric(
                team_deliveries_df[
                    batter_runs_column
                ],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    if extra_runs_column is not None:

        total_runs += (
            pd.to_numeric(
                team_deliveries_df[
                    extra_runs_column
                ],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

    return int(round(total_runs))

def calculate_team_wickets_taken(
    team: str,
    deliveries_df: pd.DataFrame,
) -> int:
    """
    Calculate wickets credited to the selected bowling team.

    Run outs, retired hurt, retired out and obstructing the
    field are excluded because they are not credited to the
    bowler or bowling attack in the same way.
    """

    if deliveries_df.empty:
        return 0

    bowling_team_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=BOWLING_TEAM_COLUMNS,
    )

    if bowling_team_column is None:
        return 0

    bowling_team_values = clean_text_series(
        deliveries_df[bowling_team_column]
    )

    team_deliveries_df = deliveries_df[
        bowling_team_values.eq(team)
    ].copy()

    if team_deliveries_df.empty:
        return 0

    dismissal_kind_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=DISMISSAL_KIND_COLUMNS,
    )

    if dismissal_kind_column is not None:
        dismissal_values = (
            clean_text_series(
                team_deliveries_df[
                    dismissal_kind_column
                ]
            )
            .str.lower()
        )

        excluded_dismissals = {
            "",
            "run out",
            "retired hurt",
            "retired out",
            "obstructing the field",
        }

        wickets_taken = int(
            (
                ~dismissal_values.isin(
                    excluded_dismissals
                )
            ).sum()
        )

        return wickets_taken

    is_wicket_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=IS_WICKET_COLUMNS,
    )

    if is_wicket_column is not None:

        wicket_values = (
            pd.to_numeric(
                team_deliveries_df[
                    is_wicket_column
                ],
                errors="coerce",
            )
            .fillna(0)
        )

        return int(
            wicket_values.eq(1).sum()
        )

    player_dismissed_column = get_optional_column(
        dataframe=team_deliveries_df,
        candidate_columns=PLAYER_DISMISSED_COLUMNS,
    )

    if player_dismissed_column is not None:

        dismissed_values = clean_text_series(
            team_deliveries_df[
                player_dismissed_column
            ]
        )

        return int(
            dismissed_values.ne("").sum()
        )

    return 0

def get_team_season_options(
    matches_df: pd.DataFrame,
    team: str,
) -> list[Any]:
    """
    Return seasons in which the selected team participated.
    """

    team_matches_df = filter_matches_for_team(
        matches_df=matches_df,
        team=team,
    )

    if team_matches_df.empty:
        return []

    season_column = get_optional_column(
        dataframe=team_matches_df,
        candidate_columns=SEASON_COLUMNS,
    )

    if season_column is None:
        return []

    seasons = (
        team_matches_df[season_column]
        .dropna()
        .unique()
        .tolist()
    )

    try:
        return sorted(seasons)
    except TypeError:
        return sorted(
            seasons,
            key=lambda value: str(value),
        )

def get_team_venue_options(
    matches_df: pd.DataFrame,
    team: str,
) -> list[str]:
    """
    Return venues where the selected team has played.
    """

    team_matches_df = filter_matches_for_team(
        matches_df=matches_df,
        team=team,
    )

    if team_matches_df.empty:
        return []

    venue_column = get_optional_column(
        dataframe=team_matches_df,
        candidate_columns=VENUE_COLUMNS,
    )

    if venue_column is None:
        return []

    venue_values = clean_text_series(
        team_matches_df[venue_column]
    )

    venues = set(
        venue_values.tolist()
    )

    venues.discard("")

    return sorted(venues)

# ==========================================================
# Season-level team performance
# ==========================================================

def create_team_season_match_summary(
    team: str,
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate season-by-season match results for a team.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Season
        - Matches
        - Wins
        - Losses
        - No Results
        - Decided Matches
        - Win Percentage
    """

    output_columns = [
        "Season",
        "Matches",
        "Wins",
        "Losses",
        "No Results",
        "Decided Matches",
        "Win Percentage",
    ]

    if matches_df.empty or not team:
        return pd.DataFrame(columns=output_columns)

    season_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=SEASON_COLUMNS,
    )

    winner_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=WINNER_COLUMNS,
    )

    if season_column is None:
        return pd.DataFrame(columns=output_columns)

    analysis_df = matches_df.copy()

    analysis_df["Season"] = (
        analysis_df[season_column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    analysis_df = analysis_df[
        analysis_df["Season"].ne("")
    ].copy()

    if analysis_df.empty:
        return pd.DataFrame(columns=output_columns)

    if winner_column is not None:

        analysis_df["_winner"] = clean_text_series(
            analysis_df[winner_column]
        )

        analysis_df["_is_win"] = (
            analysis_df["_winner"]
            .eq(team)
            .astype(int)
        )

        analysis_df["_is_no_result"] = (
            analysis_df["_winner"]
            .eq("")
            .astype(int)
        )

        analysis_df["_is_loss"] = (
            (
                analysis_df["_winner"].ne("")
                & analysis_df["_winner"].ne(team)
            )
            .astype(int)
        )

    else:

        analysis_df["_is_win"] = 0
        analysis_df["_is_loss"] = 0
        analysis_df["_is_no_result"] = 1

    summary_df = (
        analysis_df
        .groupby(
            "Season",
            dropna=False,
        )
        .agg(
            Matches=(
                "Season",
                "size",
            ),
            Wins=(
                "_is_win",
                "sum",
            ),
            Losses=(
                "_is_loss",
                "sum",
            ),
            **{
                "No Results": (
                    "_is_no_result",
                    "sum",
                ),
            },
        )
        .reset_index()
    )

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

    summary_df["Decided Matches"] = (
        summary_df["Wins"]
        + summary_df["Losses"]
    )

    summary_df["Win Percentage"] = (
        summary_df.apply(
            lambda row: round(
                safe_divide(
                    numerator=row["Wins"],
                    denominator=row["Decided Matches"],
                )
                * 100,
                1,
            ),
            axis=1,
        )
    )

    return (
        sort_season_dataframe(
            dataframe=summary_df[
                output_columns
            ],
            season_column="Season",
        )
        .reset_index(drop=True)
    )

def create_team_season_delivery_summary(
    team: str,
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate runs scored and wickets taken by season.

    Match season information is joined to deliveries using
    the match ID.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Season
        - Runs Scored
        - Wickets Taken
    """

    output_columns = [
        "Season",
        "Runs Scored",
        "Wickets Taken",
    ]

    if (
        matches_df.empty
        or deliveries_df.empty
        or not team
    ):
        return pd.DataFrame(columns=output_columns)

    match_id_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=MATCH_ID_COLUMNS,
    )

    delivery_match_id_column = get_optional_column(
        dataframe=deliveries_df,
        candidate_columns=DELIVERY_MATCH_ID_COLUMNS,
    )

    season_column = get_optional_column(
        dataframe=matches_df,
        candidate_columns=SEASON_COLUMNS,
    )

    if (
        match_id_column is None
        or delivery_match_id_column is None
        or season_column is None
    ):
        return pd.DataFrame(columns=output_columns)

    match_season_df = (
        matches_df[
            [
                match_id_column,
                season_column,
            ]
        ]
        .drop_duplicates(
            subset=[match_id_column]
        )
        .rename(
            columns={
                match_id_column: "_match_id",
                season_column: "Season",
            }
        )
    )

    match_season_df["Season"] = (
        match_season_df["Season"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    delivery_analysis_df = (
        deliveries_df
        .copy()
        .rename(
            columns={
                delivery_match_id_column: "_match_id",
            }
        )
    )

    merged_df = delivery_analysis_df.merge(
        match_season_df,
        on="_match_id",
        how="inner",
    )

    if merged_df.empty:
        return pd.DataFrame(columns=output_columns)

    runs_summary_df = create_team_runs_by_season(
        team=team,
        deliveries_df=merged_df,
    )

    wickets_summary_df = create_team_wickets_by_season(
        team=team,
        deliveries_df=merged_df,
    )

    season_values = sorted(
        set(
            runs_summary_df.get(
                "Season",
                pd.Series(dtype=str),
            ).tolist()
            + wickets_summary_df.get(
                "Season",
                pd.Series(dtype=str),
            ).tolist()
        )
    )

    if not season_values:
        return pd.DataFrame(columns=output_columns)

    summary_df = pd.DataFrame(
        {
            "Season": season_values,
        }
    )

    if not runs_summary_df.empty:

        summary_df = summary_df.merge(
            runs_summary_df,
            on="Season",
            how="left",
        )

    else:

        summary_df["Runs Scored"] = 0

    if not wickets_summary_df.empty:

        summary_df = summary_df.merge(
            wickets_summary_df,
            on="Season",
            how="left",
        )

    else:

        summary_df["Wickets Taken"] = 0

    for column in [
        "Runs Scored",
        "Wickets Taken",
    ]:

        if column not in summary_df.columns:
            summary_df[column] = 0

        summary_df[column] = (
            pd.to_numeric(
                summary_df[column],
                errors="coerce",
            )
            .fillna(0)
            .round()
            .astype(int)
        )

    return (
        sort_season_dataframe(
            dataframe=summary_df[
                output_columns
            ],
            season_column="Season",
        )
        .reset_index(drop=True)
    )

def create_team_season_performance_summary(
    team: str,
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine team match and delivery statistics by season.

    Returns
    -------
    pd.DataFrame
        Columns:
        - Season
        - Matches
        - Wins
        - Losses
        - No Results
        - Win Percentage
        - Runs Scored
        - Average Runs per Match
        - Wickets Taken
        - Average Wickets per Match
    """

    output_columns = [
        "Season",
        "Matches",
        "Wins",
        "Losses",
        "No Results",
        "Win Percentage",
        "Runs Scored",
        "Average Runs per Match",
        "Wickets Taken",
        "Average Wickets per Match",
    ]

    match_summary_df = (
        create_team_season_match_summary(
            team=team,
            matches_df=matches_df,
        )
    )

    delivery_summary_df = (
        create_team_season_delivery_summary(
            team=team,
            matches_df=matches_df,
            deliveries_df=deliveries_df,
        )
    )

    if match_summary_df.empty:
        return pd.DataFrame(columns=output_columns)

    summary_df = match_summary_df.copy()

    summary_df = summary_df.drop(
        columns=["Decided Matches"],
        errors="ignore",
    )

    if not delivery_summary_df.empty:

        summary_df = summary_df.merge(
            delivery_summary_df,
            on="Season",
            how="left",
        )

    else:

        summary_df["Runs Scored"] = 0
        summary_df["Wickets Taken"] = 0

    for column in [
        "Runs Scored",
        "Wickets Taken",
    ]:

        if column not in summary_df.columns:
            summary_df[column] = 0

        summary_df[column] = (
            pd.to_numeric(
                summary_df[column],
                errors="coerce",
            )
            .fillna(0)
            .round()
            .astype(int)
        )

    summary_df["Average Runs per Match"] = (
        summary_df.apply(
            lambda row: round(
                safe_divide(
                    numerator=row["Runs Scored"],
                    denominator=row["Matches"],
                ),
                1,
            ),
            axis=1,
        )
    )

    summary_df["Average Wickets per Match"] = (
        summary_df.apply(
            lambda row: round(
                safe_divide(
                    numerator=row["Wickets Taken"],
                    denominator=row["Matches"],
                ),
                1,
            ),
            axis=1,
        )
    )

    return (
        sort_season_dataframe(
            dataframe=summary_df[
                output_columns
            ],
            season_column="Season",
        )
        .reset_index(drop=True)
    )

