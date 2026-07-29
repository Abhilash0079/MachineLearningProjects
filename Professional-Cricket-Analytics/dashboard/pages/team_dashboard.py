"""
Team Dashboard.

Provides detailed performance analysis for one selected team.
"""

import streamlit as st

from utils.data_loader import load_all_data
from utils.page_components import display_page_header
from utils.team_analytics import (
    calculate_team_kpis,
    filter_deliveries_for_team_matches,
    filter_matches_for_team,
    get_team_options,
    get_team_season_options,
    get_team_venue_options,
)


# ==========================================================
# KPI cards
# ==========================================================

def display_team_kpis(
    team: str,
    filtered_matches_df,
    filtered_deliveries_df,
) -> None:
    """
    Display high-level team performance KPI cards.
    """

    kpis = calculate_team_kpis(
        team=team,
        matches_df=filtered_matches_df,
        deliveries_df=filtered_deliveries_df,
    )

    row_1_columns = st.columns(4)

    with row_1_columns[0]:
        st.metric(
            label="Matches",
            value=f"{kpis['matches']:,}",
        )

    with row_1_columns[1]:
        st.metric(
            label="Wins",
            value=f"{kpis['wins']:,}",
        )

    with row_1_columns[2]:
        st.metric(
            label="Losses",
            value=f"{kpis['losses']:,}",
        )

    with row_1_columns[3]:
        st.metric(
            label="Win Percentage",
            value=f"{kpis['win_percentage']:.1f}%",
        )

    row_2_columns = st.columns(4)

    with row_2_columns[0]:
        st.metric(
            label="Runs Scored",
            value=f"{kpis['runs_scored']:,}",
        )

    with row_2_columns[1]:
        st.metric(
            label="Wickets Taken",
            value=f"{kpis['wickets_taken']:,}",
        )

    with row_2_columns[2]:
        st.metric(
            label="Toss Wins",
            value=f"{kpis['toss_wins']:,}",
        )

    with row_2_columns[3]:
        st.metric(
            label="No Results",
            value=f"{kpis['no_results']:,}",
        )

# ==========================================================
# Team dashboard filters
# ==========================================================

def display_team_dashboard_filters(
    matches_df,
) -> dict[str, object]:
    """
    Display team, season and venue filters.
    """

    team_options = get_team_options(
        matches_df=matches_df,
    )

    if not team_options:

        st.error(
            "No participating teams were found "
            "in the match dataset."
        )

        st.stop()

    filter_columns = st.columns(
        [
            1.3,
            1,
            1.4,
        ]
    )

    with filter_columns[0]:

        selected_team = st.selectbox(
            label="Select Team",
            options=team_options,
            key="team_dashboard_team",
        )

    season_options = get_team_season_options(
        matches_df=matches_df,
        team=selected_team,
    )

    venue_options = get_team_venue_options(
        matches_df=matches_df,
        team=selected_team,
    )

    valid_season_options = [
        "All",
        *season_options,
    ]

    valid_venue_options = [
        "All",
        *venue_options,
    ]

    if (
        st.session_state.get(
            "team_dashboard_season"
        )
        not in valid_season_options
    ):
        st.session_state[
            "team_dashboard_season"
        ] = "All"

    if (
        st.session_state.get(
            "team_dashboard_venue"
        )
        not in valid_venue_options
    ):
        st.session_state[
            "team_dashboard_venue"
        ] = "All"

    with filter_columns[1]:

        selected_season = st.selectbox(
            label="Season",
            options=valid_season_options,
            key="team_dashboard_season",
        )

    with filter_columns[2]:

        selected_venue = st.selectbox(
            label="Venue",
            options=valid_venue_options,
            key="team_dashboard_venue",
        )

    return {
        "team": selected_team,
        "season": selected_season,
        "venue": selected_venue,
    }

# ==========================================================
# Main dashboard
# ==========================================================

def show_team_dashboard() -> None:
    """
    Render the Team Dashboard.
    """

    display_page_header(
        title="Team Dashboard",
        subtitle=(
            "Analyse team performance, season trends, "
            "opponent records and venue behaviour."
        ),
        icon="🛡️",
    )

    data = load_all_data()

    matches_df = data["matches"]
    deliveries_df = data["deliveries"]
    players_df = data["players"]

    selected_filters = (
        display_team_dashboard_filters(
            matches_df=matches_df,
        )
    )

    selected_team = selected_filters["team"]
    selected_season = selected_filters["season"]
    selected_venue = selected_filters["venue"]

    filtered_matches_df = (
        filter_matches_for_team(
            matches_df=matches_df,
            team=selected_team,
            season=selected_season,
            venue=selected_venue,
        )
    )

    filtered_deliveries_df = (
        filter_deliveries_for_team_matches(
            matches_df=filtered_matches_df,
            deliveries_df=deliveries_df,
        )
    )

    st.markdown(
        f"### {selected_team}"
    )

    active_filter_text = (
        f"Season: **{selected_season}**  |  "
        f"Venue: **{selected_venue}**"
    )

    st.caption(
        active_filter_text
    )

    if filtered_matches_df.empty:

        st.warning(
            "No matches are available for the selected "
            "team, season and venue combination."
        )

        return

    display_team_kpis(
        team=selected_team,
        filtered_matches_df=filtered_matches_df,
        filtered_deliveries_df=filtered_deliveries_df,
    )

    st.divider()

    st.info(
        "Season trends, opponent records and venue analysis "
        "will be added in the next Team Dashboard steps."
    )

show_team_dashboard()