import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_executive_dashboard() -> None:
    """
    Display the Executive Dashboard page.
    """

    display_page_header(
        title="Executive Dashboard",
        subtitle=(
            "League-level performance, competition trends "
            "and strategic cricket intelligence."
        ),
        icon="📈",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "League-wide KPI summary",
            "Matches and runs by season",
            "Team performance rankings",
            "Toss decision analysis",
            "Batting-first versus chasing outcomes",
            "Top-performing batters and bowlers",
            "Venue and match-result trends",
        ]
    )


show_executive_dashboard()