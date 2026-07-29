"""
Team Dashboard.

Provides detailed performance analysis for one selected team.
"""

import streamlit as st

from utils.data_loader import load_all_data
from utils.page_components import display_page_header
from utils.team_analytics import (
    calculate_team_kpis,
    create_team_season_performance_summary,
    filter_deliveries_for_team_matches,
    filter_deliveries_for_team_matches,
    filter_matches_for_team,
    get_team_options,
    get_team_season_options,
    get_team_venue_options,
)
from utils.charts import (
    create_bar_chart,
    create_line_chart,
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
# Season performance display
# ==========================================================

def display_team_season_performance(
    team: str,
    filtered_matches_df,
    filtered_deliveries_df,
) -> None:
    """
    Display season-by-season team performance.
    """

    st.subheader("📅 Season-by-Season Performance")

    season_summary_df = (
        create_team_season_performance_summary(
            team=team,
            matches_df=filtered_matches_df,
            deliveries_df=filtered_deliveries_df,
        )
    )

    if season_summary_df.empty:

        st.info(
            "Season performance data is not available "
            "for the selected filters."
        )

        return

    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:

        wins_figure = create_bar_chart(
            dataframe=season_summary_df,
            x_column="Season",
            y_column="Wins",
            title="Wins by Season",
            x_axis_title="Season",
            y_axis_title="Wins",
            height=450,
        )

        wins_figure.update_traces(
            texttemplate="%{y}",
            textposition="outside",
            hovertemplate=(
                "<b>Season: %{x}</b><br>"
                "Wins: %{y}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            wins_figure,
            use_container_width=True,
        )

    with chart_column_2:

        win_percentage_figure = create_line_chart(
            dataframe=season_summary_df,
            x_column="Season",
            y_column="Win Percentage",
            title="Win Percentage by Season",
            x_axis_title="Season",
            y_axis_title="Win Percentage",
            markers=True,
            height=450,
        )

        win_percentage_figure.update_traces(
            texttemplate="%{y:.1f}%",
            hovertemplate=(
                "<b>Season: %{x}</b><br>"
                "Win Percentage: %{y:.1f}%"
                "<extra></extra>"
            ),
        )

        win_percentage_figure.update_yaxes(
            ticksuffix="%",
            range=[0, 100],
        )

        st.plotly_chart(
            win_percentage_figure,
            use_container_width=True,
        )

    st.markdown("#### Match Results by Season")

    match_results_long_df = (
        season_summary_df[
            [
                "Season",
                "Wins",
                "Losses",
                "No Results",
            ]
        ]
        .melt(
            id_vars="Season",
            value_vars=[
                "Wins",
                "Losses",
                "No Results",
            ],
            var_name="Result",
            value_name="Matches",
        )
    )

    match_results_figure = create_bar_chart(
        dataframe=match_results_long_df,
        x_column="Season",
        y_column="Matches",
        color_column="Result",
        title="Wins, Losses and No Results by Season",
        x_axis_title="Season",
        y_axis_title="Matches",
        # barmode="group",
        height=500,
    )

    # match_results_figure.update_traces(
    #     hovertemplate=(
    #         "<b>Season: %{x}</b><br>"
    #         "Matches: %{y}"
    #         "<extra></extra>"
    #     ),
    # )

    st.plotly_chart(
        match_results_figure,
        use_container_width=True,
    )

    st.markdown("#### Team Output by Season")
    output_column_1, output_column_2 = st.columns(2)
    with output_column_1:

        runs_figure = create_line_chart(
            dataframe=season_summary_df,
            x_column="Season",
            y_column="Runs Scored",
            title="Runs Scored by Season",
            x_axis_title="Season",
            y_axis_title="Runs Scored",
            markers=True,
            height=450,
        )

        # runs_figure.update_traces(
        #     hovertemplate=(
        #         "<b>Season: %{x}</b><br>"
        #         "Runs Scored: %{y:,.0f}"
        #         "<extra></extra>"
        #     ),
        # )

        st.plotly_chart(
            runs_figure,
            use_container_width=True,
        )

    with output_column_2:

        wickets_figure = create_line_chart(
            dataframe=season_summary_df,
            x_column="Season",
            y_column="Wickets Taken",
            title="Wickets Taken by Season",
            x_axis_title="Season",
            y_axis_title="Wickets Taken",
            markers=True,
            height=450,
        )

        # wickets_figure.update_traces(
        #     hovertemplate=(
        #         "<b>Season: %{x}</b><br>"
        #         "Wickets Taken: %{y}"
        #         "<extra></extra>"
        #     ),
        # )

        st.plotly_chart(
            wickets_figure,
            use_container_width=True,
        )

    st.markdown("#### Season Performance Table")

    display_df = season_summary_df.copy()

    display_df["Win Percentage"] = (
        display_df["Win Percentage"]
        .map(
            lambda value: f"{value:.1f}%"
        )
    )

    display_df["Average Runs per Match"] = (
        display_df["Average Runs per Match"]
        .map(
            lambda value: f"{value:.1f}"
        )
    )

    display_df["Average Wickets per Match"] = (
        display_df["Average Wickets per Match"]
        .map(
            lambda value: f"{value:.1f}"
        )
    )

    # st.dataframe(
    #     display_df,
    #     use_container_width=True,
    #     hide_index=True,
    #     column_config={
    #         "Season": st.column_config.TextColumn(
    #             "Season",
    #             width="small",
    #         ),
    #         "Matches": st.column_config.NumberColumn(
    #             "Matches",
    #             format="%d",
    #         ),
    #         "Wins": st.column_config.NumberColumn(
    #             "Wins",
    #             format="%d",
    #         ),
    #         "Losses": st.column_config.NumberColumn(
    #             "Losses",
    #             format="%d",
    #         ),
    #         "No Results": st.column_config.NumberColumn(
    #             "No Results",
    #             format="%d",
    #         ),
    #         "Win Percentage": st.column_config.TextColumn(
    #             "Win Percentage",
    #         ),
    #         "Runs Scored": st.column_config.NumberColumn(
    #             "Runs Scored",
    #             format="%d",
    #         ),
    #         "Average Runs per Match": (
    #             st.column_config.TextColumn(
    #                 "Average Runs per Match",
    #             )
    #         ),
    #         "Wickets Taken": (
    #             st.column_config.NumberColumn(
    #                 "Wickets Taken",
    #                 format="%d",
    #             )
    #         ),
    #         "Average Wickets per Match": (
    #             st.column_config.TextColumn(
    #                 "Average Wickets per Match",
    #             )
    #         ),
    #     },
    # )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
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

    display_team_season_performance(
        team=selected_team,
        filtered_matches_df=filtered_matches_df,
        filtered_deliveries_df=filtered_deliveries_df,
    )

show_team_dashboard()