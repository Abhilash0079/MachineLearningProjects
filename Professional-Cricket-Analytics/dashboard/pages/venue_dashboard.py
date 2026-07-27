import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_venue_dashboard() -> None:
    """
    Display the Venue Dashboard page.
    """

    display_page_header(
        title="Venue Dashboard",
        subtitle=(
            "Study venue scoring patterns, match outcomes, "
            "toss strategy and ground behaviour."
        ),
        icon="🏟️",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "Matches played by venue",
            "Average first-innings score",
            "Highest and lowest team totals",
            "Batting-first versus chasing success",
            "Toss decision distribution",
            "Boundary and wicket trends",
            "Top teams at each venue",
            "Top venue performers",
        ]
    )


show_venue_dashboard()