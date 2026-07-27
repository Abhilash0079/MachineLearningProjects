from collections.abc import Sequence
from typing import Any

import pandas as pd
import streamlit as st


# ==========================================================
# Common values and column candidates
# ==========================================================

ALL_OPTION = "All"

MATCH_ID_COLUMNS = [
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

VENUE_COLUMNS = [
    "venue",
    "Venue",
    "ground",
    "stadium",
]

BATTER_COLUMNS = [
    "batter",
    "batsman",
    "striker",
]

BOWLER_COLUMNS = [
    "bowler",
]

BATTING_TEAM_COLUMNS = [
    "batting_team",
    "battingTeam",
]

BOWLING_TEAM_COLUMNS = [
    "bowling_team",
    "bowlingTeam",
]


# ==========================================================
# Column helpers
# ==========================================================

def find_first_available_column(
    dataframe: pd.DataFrame,
    candidate_columns: Sequence[str],
) -> str:
    """
    Return the first candidate column available in a DataFrame.

    Raises
    ------
    KeyError
        When none of the candidate columns exists.
    """

    for column in candidate_columns:
        if column in dataframe.columns:
            return column

    raise KeyError(
        "None of the expected columns were found. "
        f"Expected one of: {list(candidate_columns)}. "
        f"Available columns: {dataframe.columns.tolist()}"
    )


def find_optional_column(
    dataframe: pd.DataFrame,
    candidate_columns: Sequence[str],
) -> str | None:
    """
    Return the first available candidate column or None.
    """

    for column in candidate_columns:
        if column in dataframe.columns:
            return column

    return None


# ==========================================================
# Option preparation
# ==========================================================

def clean_unique_values(
    values: pd.Series,
) -> list[Any]:
    """
    Return clean, unique and sorted values from a Series.
    """

    cleaned_values = (
        values
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    cleaned_values = [
        value
        for value in cleaned_values
        if str(value).strip()
    ]

    try:
        return sorted(cleaned_values)

    except TypeError:
        return sorted(
            cleaned_values,
            key=lambda value: str(value).lower(),
        )


def add_all_option(
    options: Sequence[Any],
) -> list[Any]:
    """
    Add the All option at the beginning of an option list.
    """

    cleaned_options = [
        option
        for option in options
        if str(option).strip().lower()
        != ALL_OPTION.lower()
    ]

    return [
        ALL_OPTION,
        *cleaned_options,
    ]


def get_season_options(
    matches_df: pd.DataFrame,
) -> list[Any]:
    """
    Return all available season options.
    """

    season_column = find_first_available_column(
        matches_df,
        SEASON_COLUMNS,
    )

    return add_all_option(
        clean_unique_values(
            matches_df[season_column]
        )
    )


def get_team_options(
    matches_df: pd.DataFrame,
) -> list[str]:
    """
    Return teams appearing in either team column.
    """

    team_1_column = find_first_available_column(
        matches_df,
        TEAM_1_COLUMNS,
    )

    team_2_column = find_first_available_column(
        matches_df,
        TEAM_2_COLUMNS,
    )

    combined_teams = pd.concat(
        [
            matches_df[team_1_column],
            matches_df[team_2_column],
        ],
        ignore_index=True,
    )

    team_options = [
        str(team).strip()
        for team in clean_unique_values(
            combined_teams
        )
    ]

    return add_all_option(
        team_options
    )


def get_venue_options(
    matches_df: pd.DataFrame,
) -> list[str]:
    """
    Return all available venue options.
    """

    venue_column = find_first_available_column(
        matches_df,
        VENUE_COLUMNS,
    )

    venues = [
        str(venue).strip()
        for venue in clean_unique_values(
            matches_df[venue_column]
        )
    ]

    return add_all_option(
        venues
    )


def get_batter_options(
    deliveries_df: pd.DataFrame,
) -> list[str]:
    """
    Return all available batter options.
    """

    batter_column = find_first_available_column(
        deliveries_df,
        BATTER_COLUMNS,
    )

    batters = [
        str(batter).strip()
        for batter in clean_unique_values(
            deliveries_df[batter_column]
        )
    ]

    return add_all_option(
        batters
    )


def get_bowler_options(
    deliveries_df: pd.DataFrame,
) -> list[str]:
    """
    Return all available bowler options.
    """

    bowler_column = find_first_available_column(
        deliveries_df,
        BOWLER_COLUMNS,
    )

    bowlers = [
        str(bowler).strip()
        for bowler in clean_unique_values(
            deliveries_df[bowler_column]
        )
    ]

    return add_all_option(
        bowlers
    )


def get_match_options(
    matches_df: pd.DataFrame,
) -> list[Any]:
    """
    Return available match-ID options.
    """

    match_id_column = find_first_available_column(
        matches_df,
        MATCH_ID_COLUMNS,
    )

    return add_all_option(
        clean_unique_values(
            matches_df[match_id_column]
        )
    )


# ==========================================================
# Widget state helpers
# ==========================================================

def initialise_filter_state(
    key: str,
    options: Sequence[Any],
) -> None:
    """
    Initialise a filter key and correct invalid stored values.
    """

    if not options:
        return

    if key not in st.session_state:
        st.session_state[key] = ALL_OPTION

    if st.session_state[key] not in options:
        st.session_state[key] = ALL_OPTION


def reset_filter_state(
    key_prefix: str,
    include_player_filters: bool,
) -> None:
    """
    Reset filter-widget state to All.

    This function is used as a button callback so Streamlit updates
    the widgets safely before rerunning the page.
    """

    keys_to_reset = [
        f"{key_prefix}_season",
        f"{key_prefix}_team",
        f"{key_prefix}_venue",
    ]

    if include_player_filters:
        keys_to_reset.extend(
            [
                f"{key_prefix}_batter",
                f"{key_prefix}_bowler",
            ]
        )

    for key in keys_to_reset:
        st.session_state[key] = ALL_OPTION


# ==========================================================
# Global filter controls
# ==========================================================

def display_global_filters(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
    include_player_filters: bool = False,
    key_prefix: str = "global",
) -> dict[str, Any]:
    """
    Display reusable filters in the Streamlit sidebar.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Match-level dataset.

    deliveries_df : pd.DataFrame
        Delivery-level dataset.

    include_player_filters : bool
        Whether Batter and Bowler filters should appear.

    key_prefix : str
        Unique prefix for widget session-state keys.

    Returns
    -------
    dict
        Selected season, team, venue, batter and bowler.
    """

    season_options = get_season_options(
        matches_df
    )

    team_options = get_team_options(
        matches_df
    )

    venue_options = get_venue_options(
        matches_df
    )

    batter_options = [ALL_OPTION]
    bowler_options = [ALL_OPTION]

    if include_player_filters:
        batter_options = get_batter_options(
            deliveries_df
        )

        bowler_options = get_bowler_options(
            deliveries_df
        )

    season_key = f"{key_prefix}_season"
    team_key = f"{key_prefix}_team"
    venue_key = f"{key_prefix}_venue"
    batter_key = f"{key_prefix}_batter"
    bowler_key = f"{key_prefix}_bowler"

    initialise_filter_state(
        season_key,
        season_options,
    )

    initialise_filter_state(
        team_key,
        team_options,
    )

    initialise_filter_state(
        venue_key,
        venue_options,
    )

    if include_player_filters:
        initialise_filter_state(
            batter_key,
            batter_options,
        )

        initialise_filter_state(
            bowler_key,
            bowler_options,
        )

    with st.sidebar:

        st.divider()

        st.subheader("🔍 Filters")

        selected_season = st.selectbox(
            label="Season",
            options=season_options,
            key=season_key,
        )

        selected_team = st.selectbox(
            label="Team",
            options=team_options,
            key=team_key,
        )

        selected_venue = st.selectbox(
            label="Venue",
            options=venue_options,
            key=venue_key,
        )

        selected_batter = ALL_OPTION
        selected_bowler = ALL_OPTION

        if include_player_filters:

            selected_batter = st.selectbox(
                label="Batter",
                options=batter_options,
                key=batter_key,
            )

            selected_bowler = st.selectbox(
                label="Bowler",
                options=bowler_options,
                key=bowler_key,
            )

        st.button(
            label="Reset Filters",
            key=f"{key_prefix}_reset_filters",
            use_container_width=True,
            on_click=reset_filter_state,
            args=(
                key_prefix,
                include_player_filters,
            ),
        )

    return {
        "season": selected_season,
        "team": selected_team,
        "venue": selected_venue,
        "batter": selected_batter,
        "bowler": selected_bowler,
    }


# ==========================================================
# Match filtering
# ==========================================================

def filter_matches(
    matches_df: pd.DataFrame,
    season: Any = ALL_OPTION,
    team: str = ALL_OPTION,
    venue: str = ALL_OPTION,
) -> pd.DataFrame:
    """
    Filter match-level data by season, team and venue.
    """

    filtered_df = matches_df.copy()

    season_column = find_first_available_column(
        filtered_df,
        SEASON_COLUMNS,
    )

    team_1_column = find_first_available_column(
        filtered_df,
        TEAM_1_COLUMNS,
    )

    team_2_column = find_first_available_column(
        filtered_df,
        TEAM_2_COLUMNS,
    )

    venue_column = find_first_available_column(
        filtered_df,
        VENUE_COLUMNS,
    )

    if str(season).strip().lower() != ALL_OPTION.lower():

        selected_season = str(
            season
        ).strip()

        filtered_df = filtered_df[
            filtered_df[season_column]
            .astype(str)
            .str.strip()
            .eq(selected_season)
        ]

    if str(team).strip().lower() != ALL_OPTION.lower():

        selected_team = str(
            team
        ).strip()

        team_1_matches = (
            filtered_df[team_1_column]
            .astype(str)
            .str.strip()
            .eq(selected_team)
        )

        team_2_matches = (
            filtered_df[team_2_column]
            .astype(str)
            .str.strip()
            .eq(selected_team)
        )

        filtered_df = filtered_df[
            team_1_matches | team_2_matches
        ]

    if str(venue).strip().lower() != ALL_OPTION.lower():

        selected_venue = str(
            venue
        ).strip()

        filtered_df = filtered_df[
            filtered_df[venue_column]
            .astype(str)
            .str.strip()
            .eq(selected_venue)
        ]

    return filtered_df.reset_index(
        drop=True
    )


# ==========================================================
# Match-ID extraction
# ==========================================================

def get_filtered_match_ids(
    matches_df: pd.DataFrame,
) -> list[Any]:
    """
    Return match IDs from filtered match data.
    """

    if matches_df.empty:
        return []

    match_id_column = find_first_available_column(
        matches_df,
        MATCH_ID_COLUMNS,
    )

    return (
        matches_df[match_id_column]
        .dropna()
        .drop_duplicates()
        .tolist()
    )


# ==========================================================
# Delivery filtering
# ==========================================================

def filter_deliveries(
    deliveries_df: pd.DataFrame,
    match_ids: Sequence[Any] | None = None,
    team: str = ALL_OPTION,
    batter: str = ALL_OPTION,
    bowler: str = ALL_OPTION,
) -> pd.DataFrame:
    """
    Filter delivery-level data.

    Delivery records can be filtered by match IDs, team,
    batter and bowler.
    """

    filtered_df = deliveries_df.copy()

    delivery_match_id_column = (
        find_first_available_column(
            filtered_df,
            MATCH_ID_COLUMNS,
        )
    )

    if match_ids is not None:

        if len(match_ids) == 0:
            return filtered_df.iloc[
                0:0
            ].copy()

        filtered_df = filtered_df[
            filtered_df[
                delivery_match_id_column
            ].isin(match_ids)
        ]

    if str(team).strip().lower() != ALL_OPTION.lower():

        selected_team = str(
            team
        ).strip()

        batting_team_column = find_optional_column(
            filtered_df,
            BATTING_TEAM_COLUMNS,
        )

        bowling_team_column = find_optional_column(
            filtered_df,
            BOWLING_TEAM_COLUMNS,
        )

        team_conditions = []

        if batting_team_column is not None:
            team_conditions.append(
                filtered_df[batting_team_column]
                .astype(str)
                .str.strip()
                .eq(selected_team)
            )

        if bowling_team_column is not None:
            team_conditions.append(
                filtered_df[bowling_team_column]
                .astype(str)
                .str.strip()
                .eq(selected_team)
            )

        if team_conditions:
            combined_condition = team_conditions[0]

            for condition in team_conditions[1:]:
                combined_condition = (
                    combined_condition | condition
                )

            filtered_df = filtered_df[
                combined_condition
            ]

    if str(batter).strip().lower() != ALL_OPTION.lower():

        batter_column = find_first_available_column(
            filtered_df,
            BATTER_COLUMNS,
        )

        selected_batter = str(
            batter
        ).strip()

        filtered_df = filtered_df[
            filtered_df[batter_column]
            .astype(str)
            .str.strip()
            .eq(selected_batter)
        ]

    if str(bowler).strip().lower() != ALL_OPTION.lower():

        bowler_column = find_first_available_column(
            filtered_df,
            BOWLER_COLUMNS,
        )

        selected_bowler = str(
            bowler
        ).strip()

        filtered_df = filtered_df[
            filtered_df[bowler_column]
            .astype(str)
            .str.strip()
            .eq(selected_bowler)
        ]

    return filtered_df.reset_index(
        drop=True
    )