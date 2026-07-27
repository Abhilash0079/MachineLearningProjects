import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_batter_dashboard() -> None:
    """
    Display the Batter Dashboard page.
    """

    display_page_header(
        title="Batter Dashboard",
        subtitle=(
            "Explore batting performance, scoring patterns, "
            "consistency and phase-based effectiveness."
        ),
        icon="🏏",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "Runs and innings summary",
            "Batting average",
            "Strike rate",
            "Boundary contribution",
            "Season-wise scoring trend",
            "Powerplay, middle-over and death-over performance",
            "Dismissal analysis",
            "Venue and opposition performance",
        ]
    )


show_batter_dashboard()