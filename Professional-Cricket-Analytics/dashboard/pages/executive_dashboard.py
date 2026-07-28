import streamlit as st
from utils.data_loader import load_all_data
from utils.executive_analytics import (
    calculate_executive_kpis,
    create_innings_outcome_by_season,
    create_innings_outcome_summary,
    create_matches_by_season_summary,
    create_runs_by_season_summary,
    create_team_performance_summary,
    create_team_win_percentage_ranking,
    create_team_wins_ranking,
    create_toss_decision_summary,
    create_toss_impact_summary,
)
from utils.filters import (
    display_global_filters,
    filter_deliveries,
    filter_matches,
    get_filtered_match_ids,
)
from utils.helpers import (format_decimal, format_integer,)
from utils.page_components import (display_page_header,)
from utils.charts import (
    PLOTLY_CONFIG,
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_horizontal_bar_chart,
    apply_common_layout
)
import plotly.express as px

# ==========================================================
# Filter controls
# ==========================================================
def display_executive_filters(
    matches_df,
    deliveries_df,
) -> tuple[dict, object, object]:
    """
    Display permanent Executive Dashboard filters and apply them.
    """

    st.subheader("🔎 Dashboard Filters")

    selected_filters = display_global_filters(
        matches_df=matches_df,
        deliveries_df=deliveries_df,
        include_player_filters=False,
        key_prefix="executive",
    )

    filtered_matches_df = filter_matches(
        matches_df=matches_df,
        season=selected_filters["season"],
        team=selected_filters["team"],
        venue=selected_filters["venue"],
    )

    filtered_match_ids = get_filtered_match_ids(
        filtered_matches_df
    )

    filtered_deliveries_df = filter_deliveries(
        deliveries_df=deliveries_df,
        match_ids=filtered_match_ids,
        team=selected_filters["team"],
        batter="All",
        bowler="All",
    )

    return (
        selected_filters,
        filtered_matches_df,
        filtered_deliveries_df,
    )

# ==========================================================
# Filter summary
# ==========================================================
def display_filter_summary(
    selected_filters: dict,
) -> None:
    """
    Display a concise summary of active filters.
    """

    season = selected_filters.get(
        "season",
        "All",
    )

    team = selected_filters.get(
        "team",
        "All",
    )

    venue = selected_filters.get(
        "venue",
        "All",
    )

    st.caption(
        f"Active selection — "
        f"Season: {season} | "
        f"Team: {team} | "
        f"Venue: {venue}"
    )

# ==========================================================
# KPI cards
# ==========================================================
def display_executive_kpis(
    filtered_matches_df,
    filtered_deliveries_df,
) -> None:
    """
    Display league-level KPI cards.
    """

    kpis = calculate_executive_kpis(
        matches_df=filtered_matches_df,
        deliveries_df=filtered_deliveries_df,
    )

    st.subheader("📌 League Overview")

    first_row = st.columns(4)

    first_row[0].metric(
        label="Matches",
        value=format_integer(
            kpis["total_matches"]
        ),
    )

    first_row[1].metric(
        label="Total Runs",
        value=format_integer(
            kpis["total_runs"]
        ),
    )

    first_row[2].metric(
        label="Wickets",
        value=format_integer(
            kpis["total_wickets"]
        ),
    )

    first_row[3].metric(
        label="Participating Teams",
        value=format_integer(
            kpis["participating_teams"]
        ),
    )

    second_row = st.columns(3)

    second_row[0].metric(
        label="Completed Matches",
        value=format_integer(
            kpis["completed_matches"]
        ),
    )

    second_row[1].metric(
        label="Runs per Match",
        value=format_decimal(
            kpis["average_runs_per_match"],
            decimal_places=1,
        ),
    )

    second_row[2].metric(
        label="Wickets per Match",
        value=format_decimal(
            kpis["average_wickets_per_match"],
            decimal_places=1,
        ),
    )

# ==========================================================
# Season trend charts
# ==========================================================
def display_season_trend_charts(
    filtered_matches_df,
    filtered_deliveries_df,
) -> None:
    """
    Display match-volume and run-volume trends by season.
    """

    st.subheader("📊 Competition Trends")

    matches_summary_df = (
        create_matches_by_season_summary(
            matches_df=filtered_matches_df,
        )
    )

    runs_summary_df = (
        create_runs_by_season_summary(
            matches_df=filtered_matches_df,
            deliveries_df=filtered_deliveries_df,
        )
    )

    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:

        matches_figure = create_bar_chart(
            dataframe=matches_summary_df,
            x_column="Season",
            y_column="Matches",
            title="Matches by Season",
            x_axis_title="Season",
            y_axis_title="Matches",
            text_column="Matches",
            sort_by="Season",
            ascending=True,
            height=430,
        )

        st.plotly_chart(
            matches_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

    with chart_column_2:

        runs_figure = create_line_chart(
            dataframe=runs_summary_df,
            x_column="Season",
            y_column="Runs",
            title="Total Runs by Season",
            x_axis_title="Season",
            y_axis_title="Runs",
            markers=True,
            height=430,
        )

        st.plotly_chart(
            runs_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

# ==========================================================
# Team performance analysis
# ==========================================================
def display_team_performance_analysis(
    filtered_matches_df,
) -> None:
    """
    Display team rankings and win-percentage analysis.
    """

    st.subheader("🏆 Team Performance Rankings")

    team_summary_df = (
        create_team_performance_summary(
            matches_df=filtered_matches_df,
        )
    )

    if team_summary_df.empty:

        st.warning(
            "Team performance data is not available "
            "for the selected filters."
        )

        return

    team_wins_df = create_team_wins_ranking(
        team_summary_df=team_summary_df,
        top_n=10,
    )

    win_percentage_df = (
        create_team_win_percentage_ranking(
            team_summary_df=team_summary_df,
            minimum_matches=1,
            top_n=10,
        )
    )

    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:

        wins_figure = create_horizontal_bar_chart(
            dataframe=team_wins_df,
            category_column="Team",
            value_column="Wins",
            title="Top Teams by Match Wins",
            x_axis_title="Wins",
            y_axis_title="Team",
            top_n=10,
            ascending=True,
            height=500,
        )

        st.plotly_chart(
            wins_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

    with chart_column_2:

        win_percentage_figure = (
            create_horizontal_bar_chart(
                dataframe=win_percentage_df,
                category_column="Team",
                value_column="Win Percentage",
                title="Team Win Percentage",
                x_axis_title="Win Percentage (%)",
                y_axis_title="Team",
                top_n=10,
                ascending=True,
                height=500,
            )
        )

        win_percentage_figure.update_traces(
            texttemplate="%{x:.1f}%",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Win Percentage: %{x:.1f}%"
                "<extra></extra>"
            ),
        )

        win_percentage_figure.update_xaxes(
            ticksuffix="%",
        )

        st.plotly_chart(
            win_percentage_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

    st.markdown("#### Team Performance Table")

    display_team_summary_df = (
        team_summary_df.copy()
    )

    display_team_summary_df[
        "Win Percentage"
    ] = (
        display_team_summary_df[
            "Win Percentage"
        ]
        .map(
            lambda value: f"{value:.1f}%"
        )
    )

    st.dataframe(
        display_team_summary_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Team": st.column_config.TextColumn(
                "Team",
                width="large",
            ),
            "Matches": st.column_config.NumberColumn(
                "Matches",
                format="%d",
            ),
            "Wins": st.column_config.NumberColumn(
                "Wins",
                format="%d",
            ),
            "Losses": st.column_config.NumberColumn(
                "Losses",
                format="%d",
            ),
            "No Results": st.column_config.NumberColumn(
                "No Results",
                format="%d",
            ),
            "Win Percentage": st.column_config.TextColumn(
                "Win Percentage",
            ),
        },
    )

# ==========================================================
# Toss analysis display
# ==========================================================
def display_toss_analysis(
    filtered_matches_df,
) -> None:
    """
    Display toss-decision and toss-impact analysis.
    """

    st.subheader("🪙 Toss Analysis")

    toss_decision_df = (
        create_toss_decision_summary(
            matches_df=filtered_matches_df,
        )
    )

    toss_impact_df = (
        create_toss_impact_summary(
            matches_df=filtered_matches_df,
        )
    )

    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:

        if toss_decision_df.empty:

            st.info(
                "Toss-decision data is not available "
                "for the selected filters."
            )

        else:

            toss_decision_figure = create_pie_chart(
                dataframe=toss_decision_df,
                names_column="Toss Decision",
                values_column="Matches",
                title="Toss Decision Distribution",
                hole=0.55,
                height=430,
            )

            toss_decision_figure.update_traces(
                texttemplate=(
                    "%{label}<br>"
                    "%{value} matches<br>"
                    "%{percent}"
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Matches: %{value}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                toss_decision_figure,
                use_container_width=True,
                config=PLOTLY_CONFIG,
            )

    with chart_column_2:

        if toss_impact_df.empty:

            st.info(
                "Toss-impact data is not available "
                "for the selected filters."
            )

        else:

            toss_impact_figure = (
                create_horizontal_bar_chart(
                    dataframe=toss_impact_df,
                    category_column="Outcome",
                    value_column="Percentage",
                    title="Did the Toss Winner Win the Match?",
                    x_axis_title="Percentage (%)",
                    y_axis_title="Outcome",
                    top_n=2,
                    ascending=True,
                    height=430,
                )
            )

            toss_impact_figure.update_traces(
                texttemplate="%{x:.1f}%",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Percentage: %{x:.1f}%"
                    "<extra></extra>"
                ),
            )

            toss_impact_figure.update_xaxes(
                ticksuffix="%",
                range=[0, 100],
            )

            st.plotly_chart(
                toss_impact_figure,
                use_container_width=True,
                config=PLOTLY_CONFIG,
            )

# ==========================================================
# Innings outcome display
# ==========================================================
def display_innings_outcome_analysis(
    filtered_matches_df,
) -> None:
    """
    Display batting-first versus chasing outcomes.
    """

    st.subheader(
        "🏏 Batting First vs Chasing Outcomes"
    )

    outcome_summary_df = (
        create_innings_outcome_summary(
            matches_df=filtered_matches_df,
        )
    )

    outcome_by_season_df = (
        create_innings_outcome_by_season(
            matches_df=filtered_matches_df,
        )
    )

    chart_column_1, chart_column_2 = st.columns(
        [
            0.8,
            1.2,
        ]
    )

    with chart_column_1:

        if outcome_summary_df.empty:

            st.info(
                "Match outcome data is not available "
                "for the selected filters."
            )

        else:

            outcome_figure = create_pie_chart(
                dataframe=outcome_summary_df,
                names_column="Match Outcome",
                values_column="Matches",
                title="Overall Match Outcome Distribution",
                hole=0.50,
                height=450,
            )

            outcome_figure.update_traces(
                texttemplate=(
                    "%{label}<br>"
                    "%{value}<br>"
                    "%{percent}"
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Matches: %{value}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                outcome_figure,
                use_container_width=True,
                config=PLOTLY_CONFIG,
            )

    with chart_column_2:

        if outcome_by_season_df.empty:

            st.info(
                "Season-level outcome data is not available "
                "for the selected filters."
            )

        else:

            season_outcome_figure = px.bar(
                outcome_by_season_df,
                x="Season",
                y="Matches",
                color="Match Outcome",
                barmode="group",
                text="Matches",
                title=(
                    "Batting First and Chasing Wins "
                    "by Season"
                ),
            )

            season_outcome_figure.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>Season: %{x}</b><br>"
                    "Matches: %{y}<br>"
                    "Outcome: %{fullData.name}"
                    "<extra></extra>"
                ),
            )

            season_outcome_figure = apply_common_layout(
                figure=season_outcome_figure,
                title=(
                    "Batting First and Chasing Wins "
                    "by Season"
                ),
                height=450,
            )

            st.plotly_chart(
                season_outcome_figure,
                use_container_width=True,
                config=PLOTLY_CONFIG,
            )

# ==========================================================
# Main page
# ==========================================================
def show_executive_dashboard() -> None:
    """
    Display the Executive Dashboard.
    """

    display_page_header(
        title="Executive Dashboard",
        subtitle=(
            "League-level performance, competition trends "
            "and strategic cricket intelligence."
        ),
        icon="📈",
    )

    try:
        data = load_all_data()

        matches_df = data["matches"]
        deliveries_df = data["deliveries"]

        (
            selected_filters,
            filtered_matches_df,
            filtered_deliveries_df,
        ) = display_executive_filters(
            matches_df=matches_df,
            deliveries_df=deliveries_df,
        )

        display_filter_summary(
            selected_filters
        )

        if filtered_matches_df.empty:

            st.warning(
                "No matches are available for the selected "
                "combination of filters."
            )

            st.stop()

        display_executive_kpis(
            filtered_matches_df=filtered_matches_df,
            filtered_deliveries_df=filtered_deliveries_df,
        )

        st.divider()

        display_season_trend_charts(
            filtered_matches_df=filtered_matches_df,
            filtered_deliveries_df=filtered_deliveries_df,
        )
        st.divider()

        display_team_performance_analysis(
            filtered_matches_df=filtered_matches_df,
        )
        st.divider()

        display_toss_analysis(
            filtered_matches_df=filtered_matches_df,
        )

        st.divider()

        display_innings_outcome_analysis(
            filtered_matches_df=filtered_matches_df,
        )
        
    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        TypeError,
        RuntimeError,
    ) as error:

        st.error(
            f"Executive Dashboard could not be loaded: {error}"
        )

show_executive_dashboard()