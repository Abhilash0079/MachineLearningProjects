from pathlib import Path
import streamlit as st
import pandas as pd
from config import ( APP_NAME, APP_SUBTITLE, PAGE_TITLE, PAGE_ICON)
from utils.data_loader import load_all_data

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

        The platform enables users to analyse:

        - League-level trends
        - Team performance
        - Batter performance
        - Bowler performance
        - Venue and match conditions
        - Individual match progression
        - Partnerships and player combinations
        - Match phases and pressure situations
        """
    )

    st.divider()

    display_project_overview()
    display_data_status()
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