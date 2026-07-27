from pathlib import Path
import streamlit as st
import pandas as pd
from config import ( APP_NAME, APP_SUBTITLE, PAGE_TITLE, PAGE_ICON)
from utils.data_loader import load_all_data
from utils.filters import (
    display_global_filters,
    filter_deliveries,
    filter_matches,
    get_filtered_match_ids,
)
from utils.charts import (
    PLOTLY_CONFIG,
    create_bar_chart,
    create_horizontal_bar_chart,
    create_line_chart,
    create_pie_chart,
)

# --------------------------------------
# Application Paths
# --------------------------------------
DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent
ASSETS_DIR = DASHBOARD_DIR/'assets'

# --------------------------------------
# Streamlit page configuration
# --------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------
# Home page
# --------------------------------------
def show_home_page() -> None:
    """
    Display the main landing page of the cricket analytics dashboard.
    """
    st.title(APP_NAME)
    st.subheader(APP_SUBTITLE)
    st.markdown(
        """
        CricVision AI converts historical IPL match data into
        interactive cricket intelligence.
        """
    )

    st.divider()

    display_project_overview()
    display_data_status()
    # display_filter_test()
    display_chart_utility_test()
    display_dashboard_navigation()
    display_project_status()


def display_project_overview()-> None:
    """
    Display a brief overview using dashboard information cards.
    """

    st.subheader("📊 Platform Overview")

    column_1, column_2, column_3 = st.columns(3)

    with column_1:
        st.info(
            """
            ### Data Engineering

            Raw IPL JSON files are converted into structured
            match, delivery and player datasets.
            """
        )

    with column_2:
        st.info(
            """
            ### Cricket Analytics

            Match, team, player, venue, partnership and pressure
            performance are analysed.
            """
        )

    with column_3:
        st.info(
            """
            ### Decision Support

            Analytical findings support team selection, auctions
            and match strategy.
            """
        )

def display_dashboard_navigation() -> None:
    """
    Display the dashboards planned for the application.
    """

    st.subheader("🧭 Dashboard Navigation")

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown(
            """
            #### Executive Dashboard

            View league-wide KPIs, trends and major findings.

            #### Team Dashboard

            Compare team records, opponents, venues and seasons.

            #### Batter Dashboard

            Explore runs, averages, strike rates and phase
            performance.
            """
        )

    with right_column:
        st.markdown(
            """
            #### Bowler Dashboard

            Analyse wickets, economy, strike rate and bowling
            phases.

            #### Venue Dashboard

            Examine scoring conditions and chasing success.

            #### Match Dashboard

            Explore innings progression, wickets, partnerships
            and momentum.
            """
        )

def display_project_status() -> None:
    """
    Display the current development status of the platform.
    """

    st.subheader("🚀 Project Development Status")

    st.progress(
        40,
        text="Modules 1 and 2 completed — Dashboard development started"
    )

    st.success(
        """
        **Completed**

        Module 1 — Data Engineering

        Module 2 — Exploratory Data Analysis
        """
    )

    st.warning(
        """
        **In Progress**

        Module 3 — Interactive Dashboards
        """
    )

def display_data_status() -> None:
    """
    Load the processed datasets and display their status.
    """

    st.subheader("📁 Dataset Status")

    try:
        data = load_all_data()

        matches_df = data["matches"]
        deliveries_df = data["deliveries"]
        players_df = data["players"]

        column_1, column_2, column_3 = st.columns(3)

        with column_1:
            st.metric(
                label="Match Records",
                value=f"{len(matches_df):,}"
            )

        with column_2:
            st.metric(
                label="Delivery Records",
                value=f"{len(deliveries_df):,}"
            )

        with column_3:
            st.metric(
                label="Player Records",
                value=f"{len(players_df):,}"
            )

        st.success(
            "All processed datasets loaded successfully."
        )

    except FileNotFoundError as error:
        st.error(str(error))

    except ValueError as error:
        st.error(str(error))

    except pd.errors.ParserError as error:
        st.error(
            f"One of the CSV files could not be parsed: {error}"
        )

    except Exception as error:
        st.error(
            f"An unexpected data-loading error occurred: {error}"
        )

def display_filter_test() -> None:
    """
    Test shared dashboard filters using the processed datasets.
    """

    st.subheader("🧪 Filter Utility Test")

    try:
        data = load_all_data()

        matches_df = data["matches"]
        deliveries_df = data["deliveries"]

        selected_filters = display_global_filters(
            matches_df=matches_df,
            deliveries_df=deliveries_df,
            key_prefix="home",
            include_player_filters=False
        )

        filtered_matches_df = filter_matches(
            matches_df=matches_df,
            season=selected_filters["season"],
            team=selected_filters["team"],
            venue=selected_filters["venue"]
        )

        filtered_match_ids = get_filtered_match_ids(
            filtered_matches_df
        )

        filtered_deliveries_df = filter_deliveries(
            deliveries_df=deliveries_df,
            match_ids=filtered_match_ids,
            team=selected_filters["team"]
            # batter=selected_filters["batter"],
            # bowler=selected_filters["bowler"]
        )

        column_1, column_2 = st.columns(2)

        with column_1:
            st.metric(
                label="Filtered Matches",
                value=f"{len(filtered_matches_df):,}"
            )

        with column_2:
            st.metric(
                label="Filtered Deliveries",
                value=f"{len(filtered_deliveries_df):,}"
            )

        st.markdown("#### Active Filters")

        st.json(selected_filters)

    except Exception as error:
        st.error(
            f"Filter test failed: {error}"
        )

def display_chart_utility_test() -> None:
    """
    Test the reusable Plotly chart utility functions.
    """

    st.subheader("📊 Chart Utility Test")

    try:
        data = load_all_data()

        matches_df = data["matches"]

        season_column = (
            "season"
            if "season" in matches_df.columns
            else "Season"
        )

        season_summary = (
            matches_df
            .groupby(season_column)
            .size()
            .reset_index(name="Matches")
        )

        bar_figure = create_bar_chart(
            dataframe=season_summary,
            x_column=season_column,
            y_column="Matches",
            title="Matches by Season",
            x_axis_title="Season",
            y_axis_title="Matches",
            text_column="Matches",
            sort_by=season_column,
            ascending=True,
        )

        st.plotly_chart(
            bar_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

        line_figure = create_line_chart(
            dataframe=season_summary,
            x_column=season_column,
            y_column="Matches",
            title="Match Trend by Season",
            x_axis_title="Season",
            y_axis_title="Matches",
        )

        st.plotly_chart(
            line_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

    except Exception as error:
        st.error(
            f"Chart utility test failed: {error}"
        )

    if "winner" in matches_df.columns:
        team_wins = (
            matches_df["winner"]
            .dropna()
            .value_counts()
            .rename_axis("Team")
            .reset_index(name="Wins")
        )

        ranking_figure = create_horizontal_bar_chart(
            dataframe=team_wins,
            category_column="Team",
            value_column="Wins",
            title="Top Teams by Match Wins",
            x_axis_title="Wins",
            y_axis_title="Team",
            top_n=10,
        )

        st.plotly_chart(
            ranking_figure,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

def display_sidebar() -> None:
    """
    Display common information in the application sidebar.
    """

    with st.sidebar:
        st.title("🏏 CricVision AI")

        st.caption(
            "Professional Cricket Analytics Platform"
        )

        st.divider()

        st.markdown(
            """
            ### Current Module

            **Module 3: Interactive Dashboards**

            The application will contain six analytical
            dashboards.
            """
        )

        st.divider()

        st.markdown(
            """
            ### Data Sources

            - `matches.csv`
            - `deliveries.csv`
            - `players.csv`
            """
        )

        st.divider()

        st.caption(
            "Built using Python, Pandas, Plotly and Streamlit."
        )

# ---------------------------------------------------------
# Application navigation
# ---------------------------------------------------------

display_sidebar()

home_page = st.Page(
    show_home_page,
    title="Home",
    icon="🏠",
    default=True
)

navigation = st.navigation(
    {
        "CricVision AI": [
            home_page
        ]
    }
)

navigation.run()