import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_team_dashboard() -> None:
    """
    Display the Team Dashboard page.
    """

    display_page_header(
        title="Team Dashboard",
        subtitle=(
            "Analyse team performance, match outcomes, "
            "season trends and opposition records."
        ),
        icon="🛡️",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "Team match and win summary",
            "Season-wise performance",
            "Win percentage trend",
            "Home and venue performance",
            "Head-to-head team analysis",
            "Batting-first and chasing records",
            "Top batters and bowlers by team",
        ]
    )


show_team_dashboard()