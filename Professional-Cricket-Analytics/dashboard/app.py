from pathlib import Path
import streamlit as st

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
    page_title="CricVision AI",
    page_icon="🏏",
    layout='wide',
    initial_sidebar_state='expanded'
)

# --------------------------------------
# Home page
# --------------------------------------
def show_home_page() -> None:
    """
    Display the main landing page of the cricket analytics dashboard.
    """
    st.title("🏏 CricVision AI")

    st.subheader(
        "Professional Cricket Analytics and "
        "Decision-Support Platform"
    )
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