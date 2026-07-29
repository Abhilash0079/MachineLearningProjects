from pathlib import Path
import streamlit as st
from config import (APP_NAME, PAGE_ICON, PAGE_TITLE)
from utils.data_loader import load_all_data
from utils.helpers import (create_information_card, create_page_header, format_integer)
from utils.style_loader import load_custom_css

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

# ==========================================================
# Custom styling
# ==========================================================
try:
    load_custom_css()

except (FileNotFoundError, ValueError) as error:
    st.warning(
        f"Custom styling could not be loaded: {error}"
    )

# ==========================================================
# Home page components
# ==========================================================

def display_project_overview() -> None:
    """
    Display the main platform capabilities.
    """
    st.subheader("📊 Platform Overview")
    column_1, column_2, column_3 = st.columns(3)
    with column_1:
        st.html(
            create_information_card(
                title="Data Engineering",
                description=(
                    "Raw IPL JSON files are validated and "
                    "converted into structured match, delivery "
                    "and player datasets."
                ),
                icon="⚙️",
            )
        )

    with column_2:
        st.html(
            create_information_card(
                title="Cricket Analytics",
                description=(
                    "Explore match, team, batter, bowler, "
                    "venue, partnership and pressure analytics."
                ),
                icon="📊",
            )
        )

    with column_3:
        st.html(
            create_information_card(
                title="Decision Support",
                description=(
                    "Support auction planning, player selection, "
                    "venue strategy and match preparation."
                ),
                icon="🎯",
            )
        )


def display_data_status() -> None:
    """
    Display processed dataset status.
    """

    st.subheader("📁 Processed Data Status")

    try:
        data = load_all_data()

        matches_df = data["matches"]
        deliveries_df = data["deliveries"]
        players_df = data["players"]

        column_1, column_2, column_3 = st.columns(3)

        column_1.metric(
            label="Matches",
            value=format_integer(
                len(matches_df)
            ),
        )

        column_2.metric(
            label="Deliveries",
            value=format_integer(
                len(deliveries_df)
            ),
        )

        column_3.metric(
            label="Players",
            value=format_integer(
                len(players_df)
            ),
        )

        st.success(
            "All processed datasets loaded successfully."
        )

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        RuntimeError,
    ) as error:

        st.error(
            f"Processed data could not be loaded: {error}"
        )

def display_dashboard_navigation() -> None:
    """
    Explain the available dashboard sections.
    """

    st.subheader("🧭 Analytics Dashboards")

    st.markdown(
        """
        Use the navigation menu to explore:

        - Executive intelligence
        - Team performance
        - Batter analysis
        - Bowler analysis
        - Venue intelligence
        - Individual match analysis
        """
    )

def display_project_status() -> None:
    """
    Display current platform development status.
    """

    st.subheader("🚀 Project Status")

    st.markdown(
        """
        **Completed**

        - Data engineering pipeline
        - Processed analytical datasets
        - Exploratory data analysis
        - Shared dashboard utilities
        - Shared chart components
        - Application theme and styling
        - Multipage application foundation

        **Current phase**

        - Dashboard analytics development
        """
    )

def show_home_page() -> None:
    """
    Display the application landing page.
    """

    st.html(
        create_page_header(
            title=APP_NAME,
            subtitle=(
                "Professional Cricket Analytics and "
                "Decision-Support Platform"
            ),
            icon="🏏",
        )
    )

    st.markdown(
        """
        CricVision AI converts historical IPL match data into
        interactive cricket intelligence.

        The platform enables users to explore league, team,
        player, venue and match-level performance.
        """
    )

    st.divider()

    display_project_overview()
    display_data_status()
    display_dashboard_navigation()
    display_project_status()

# ==========================================================
# Navigation
# ==========================================================

home_page = st.Page(
    show_home_page,
    title="Home",
    icon="🏠",
    url_path="home",
    default=True,
)

executive_page = st.Page(
    "pages/executive_dashboard.py",
    title="Executive Dashboard",
    icon="📈",
    url_path="executive",
)

team_page = st.Page(
    "pages/team_dashboard.py",
    title="Team Dashboard",
    icon="🛡️",
    url_path="team",
)

batter_page = st.Page(
    "pages/batter_dashboard.py",
    title="Batter Dashboard",
    icon="🏏",
    url_path="batter",
)

bowler_page = st.Page(
    "pages/bowler_dashboard.py",
    title="Bowler Dashboard",
    icon="🎯",
    url_path="bowler",
)

venue_page = st.Page(
    "pages/venue_dashboard.py",
    title="Venue Dashboard",
    icon="🏟️",
    url_path="venue",
)

match_page = st.Page(
    "pages/match_dashboard.py",
    title="Match Dashboard",
    icon="🔍",
    url_path="match",
)


navigation = st.navigation(
    {
        "Platform": [
            home_page,
            executive_page,
        ],
        "Performance Analytics": [
            team_page,
            batter_page,
            bowler_page,
        ],
        "Match Intelligence": [
            venue_page,
            match_page,
        ],
    }
)

navigation.run()