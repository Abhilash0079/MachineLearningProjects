from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

from config import (
    DEFAULT_BATTER,
    DEFAULT_BOWLER,
    DEFAULT_SEASON,
    DEFAULT_TEAM,
    DEFAULT_VENUE,
)

from utils.helpers import (
    add_all_option,
    clean_unique_values,
    validate_required_columns,
)


# ==========================================================
# Internal column helpers
# ==========================================================

def find_first_available_column(
    dataframe: pd.DataFrame,
    possible_columns: List[str]
) -> Optional[str]:
    """
    Return the first column from possible_columns that exists
    in the supplied DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset in which columns are searched.

    possible_columns : List[str]
        Possible column names in priority order.

    Returns
    -------
    Optional[str]
        First matching column name or None.
    """

    for column in possible_columns:
        if column in dataframe.columns:
            return column

    return None


# ==========================================================
# Season options
# ==========================================================

def get_season_options(
    matches_df: pd.DataFrame
) -> List[Any]:
    """
    Return available season values with an All option.
    """

    season_column = find_first_available_column(
        matches_df,
        ["season", "Season"]
    )

    if season_column is None:
        return [DEFAULT_SEASON]

    seasons = clean_unique_values(
        matches_df[season_column]
    )

    return add_all_option(
        seasons,
        all_label=DEFAULT_SEASON
    )


# ==========================================================
# Team options
# ==========================================================

def get_team_options(
    matches_df: pd.DataFrame,
    deliveries_df: Optional[pd.DataFrame] = None
) -> List[str]:
    """
    Return all team names found in match and delivery datasets.
    """

    teams = []

    match_team_columns = [
        "team1",
        "team2",
        "winner",
        "toss_winner"
    ]

    for column in match_team_columns:
        if column in matches_df.columns:
            teams.extend(
                matches_df[column].dropna().tolist()
            )

    if deliveries_df is not None:

        delivery_team_columns = [
            "batting_team",
            "bowling_team"
        ]

        for column in delivery_team_columns:
            if column in deliveries_df.columns:
                teams.extend(
                    deliveries_df[column].dropna().tolist()
                )

    cleaned_teams = clean_unique_values(teams)

    return add_all_option(
        cleaned_teams,
        all_label=DEFAULT_TEAM
    )


# ==========================================================
# Venue options
# ==========================================================

def get_venue_options(
    matches_df: pd.DataFrame
) -> List[str]:
    """
    Return available venue names with an All option.
    """

    venue_column = find_first_available_column(
        matches_df,
        ["venue", "Venue"]
    )

    if venue_column is None:
        return [DEFAULT_VENUE]

    venues = clean_unique_values(
        matches_df[venue_column]
    )

    return add_all_option(
        venues,
        all_label=DEFAULT_VENUE
    )


# ==========================================================
# Batter options
# ==========================================================

def get_batter_options(
    deliveries_df: pd.DataFrame
) -> List[str]:
    """
    Return available batter names with an All option.
    """

    batter_column = find_first_available_column(
        deliveries_df,
        [
            "batter",
            "batsman",
            "striker"
        ]
    )

    if batter_column is None:
        return [DEFAULT_BATTER]

    batters = clean_unique_values(
        deliveries_df[batter_column]
    )

    return add_all_option(
        batters,
        all_label=DEFAULT_BATTER
    )


# ==========================================================
# Bowler options
# ==========================================================

def get_bowler_options(
    deliveries_df: pd.DataFrame
) -> List[str]:
    """
    Return available bowler names with an All option.
    """

    bowler_column = find_first_available_column(
        deliveries_df,
        ["bowler"]
    )

    if bowler_column is None:
        return [DEFAULT_BOWLER]

    bowlers = clean_unique_values(
        deliveries_df[bowler_column]
    )

    return add_all_option(
        bowlers,
        all_label=DEFAULT_BOWLER
    )


# ==========================================================
# Match options
# ==========================================================

def get_match_options(
    matches_df: pd.DataFrame
) -> List[Any]:
    """
    Return match identifiers for the match explorer.
    """

    match_id_column = find_first_available_column(
        matches_df,
        [
            "match_id",
            "id",
            "registry_id"
        ]
    )

    if match_id_column is None:
        return []

    return clean_unique_values(
        matches_df[match_id_column]
    )


# ==========================================================
# Match-level filtering
# ==========================================================

def filter_matches(
    matches_df: pd.DataFrame,
    season: Any = DEFAULT_SEASON,
    team: str = DEFAULT_TEAM,
    venue: str = DEFAULT_VENUE
) -> pd.DataFrame:
    """
    Filter the match-level dataset by season, team and venue.

    A copy of the filtered dataset is returned to avoid modifying
    the original cached DataFrame.
    """

    filtered_df = matches_df.copy()

    season_column = find_first_available_column(
        filtered_df,
        ["season", "Season"]
    )

    venue_column = find_first_available_column(
        filtered_df,
        ["venue", "Venue"]
    )

    if (
        season != DEFAULT_SEASON
        and season_column is not None
    ):
        filtered_df = filtered_df[
            filtered_df[season_column] == season
        ]

    if team != DEFAULT_TEAM:

        available_team_columns = [
            column
            for column in ["team1", "team2"]
            if column in filtered_df.columns
        ]

        if available_team_columns:
            team_mask = pd.Series(
                False,
                index=filtered_df.index
            )

            for column in available_team_columns:
                team_mask = (
                    team_mask
                    | filtered_df[column].eq(team)
                )

            filtered_df = filtered_df[team_mask]

    if (
        venue != DEFAULT_VENUE
        and venue_column is not None
    ):
        filtered_df = filtered_df[
            filtered_df[venue_column] == venue
        ]

    return filtered_df.copy()


# ==========================================================
# Delivery-level filtering
# ==========================================================

def filter_deliveries(
    deliveries_df: pd.DataFrame,
    match_ids: Optional[List[Any]] = None,
    team: str = DEFAULT_TEAM,
    batter: str = DEFAULT_BATTER,
    bowler: str = DEFAULT_BOWLER
) -> pd.DataFrame:
    """
    Filter the delivery-level dataset.

    Parameters
    ----------
    deliveries_df : pd.DataFrame
        Ball-by-ball dataset.

    match_ids : Optional[List[Any]]
        Match identifiers retained after applying match-level
        filters.

    team : str
        Team selected by the user.

    batter : str
        Batter selected by the user.

    bowler : str
        Bowler selected by the user.

    Returns
    -------
    pd.DataFrame
        Filtered delivery-level dataset.
    """

    filtered_df = deliveries_df.copy()

    delivery_match_id_column = find_first_available_column(
        filtered_df,
        [
            "match_id",
            "id",
            "registry_id"
        ]
    )

    if (
        match_ids is not None
        and delivery_match_id_column is not None
    ):
        filtered_df = filtered_df[
            filtered_df[
                delivery_match_id_column
            ].isin(match_ids)
        ]

    if team != DEFAULT_TEAM:

        available_team_columns = [
            column
            for column in [
                "batting_team",
                "bowling_team"
            ]
            if column in filtered_df.columns
        ]

        if available_team_columns:
            team_mask = pd.Series(
                False,
                index=filtered_df.index
            )

            for column in available_team_columns:
                team_mask = (
                    team_mask
                    | filtered_df[column].eq(team)
                )

            filtered_df = filtered_df[team_mask]

    batter_column = find_first_available_column(
        filtered_df,
        [
            "batter",
            "batsman",
            "striker"
        ]
    )

    if (
        batter != DEFAULT_BATTER
        and batter_column is not None
    ):
        filtered_df = filtered_df[
            filtered_df[batter_column] == batter
        ]

    bowler_column = find_first_available_column(
        filtered_df,
        ["bowler"]
    )

    if (
        bowler != DEFAULT_BOWLER
        and bowler_column is not None
    ):
        filtered_df = filtered_df[
            filtered_df[bowler_column] == bowler
        ]

    return filtered_df.copy()


# ==========================================================
# Match ID extraction
# ==========================================================

def get_filtered_match_ids(
    matches_df: pd.DataFrame
) -> Optional[List[Any]]:
    """
    Extract match identifiers from a filtered match dataset.
    """

    match_id_column = find_first_available_column(
        matches_df,
        [
            "match_id",
            "id",
            "registry_id"
        ]
    )

    if match_id_column is None:
        return None

    return (
        matches_df[match_id_column]
        .dropna()
        .unique()
        .tolist()
    )


# ==========================================================
# Shared sidebar filters
# ==========================================================

def display_global_filters(
    matches_df: pd.DataFrame,
    deliveries_df: pd.DataFrame,
    key_prefix: str = "global",
    include_player_filters: bool = False
) -> Dict[str, Any]:
    """
    Display reusable dashboard filters in the Streamlit sidebar.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Match-level dataset.

    deliveries_df : pd.DataFrame
        Ball-by-ball dataset.

    key_prefix : str, default="global"
        Unique prefix used for Streamlit widget keys.

    include_player_filters : bool, default=False
        Whether batter and bowler filters should be shown.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing selected filter values.
    """

    season_options = get_season_options(matches_df)

    team_options = get_team_options(
        matches_df=matches_df,
        deliveries_df=deliveries_df
    )

    venue_options = get_venue_options(matches_df)

    with st.sidebar:

        st.subheader("🔍 Filters")

        selected_season = st.selectbox(
            label="Season",
            options=season_options,
            index=0,
            key=f"{key_prefix}_season"
        )

        selected_team = st.selectbox(
            label="Team",
            options=team_options,
            index=0,
            key=f"{key_prefix}_team"
        )

        selected_venue = st.selectbox(
            label="Venue",
            options=venue_options,
            index=0,
            key=f"{key_prefix}_venue"
        )

        selected_batter = DEFAULT_BATTER
        selected_bowler = DEFAULT_BOWLER

        if include_player_filters:

            batter_options = get_batter_options(
                deliveries_df
            )

            bowler_options = get_bowler_options(
                deliveries_df
            )

            selected_batter = st.selectbox(
                label="Batter",
                options=batter_options,
                index=0,
                key=f"{key_prefix}_batter"
            )

            selected_bowler = st.selectbox(
                label="Bowler",
                options=bowler_options,
                index=0,
                key=f"{key_prefix}_bowler"
            )

        if st.button(
            "Reset Filters",
            key=f"{key_prefix}_reset",
            use_container_width=True
        ):
            keys_to_clear = [
                f"{key_prefix}_season",
                f"{key_prefix}_team",
                f"{key_prefix}_venue",
                f"{key_prefix}_batter",
                f"{key_prefix}_bowler",
            ]

            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    return {
        "season": selected_season,
        "team": selected_team,
        "venue": selected_venue,
        "batter": selected_batter,
        "bowler": selected_bowler,
    }