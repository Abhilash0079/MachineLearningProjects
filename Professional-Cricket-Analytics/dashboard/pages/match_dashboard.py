import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_match_dashboard() -> None:
    """
    Display the Match Dashboard page.
    """

    display_page_header(
        title="Match Dashboard",
        subtitle=(
            "Inspect individual matches through innings, "
            "partnership, phase and player-level analysis."
        ),
        icon="🔍",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "Match summary and result",
            "Team innings comparison",
            "Over-by-over scoring progression",
            "Run-rate analysis",
            "Wicket timeline",
            "Partnership analysis",
            "Batter scorecards",
            "Bowler figures",
            "Match phase comparison",
        ]
    )


show_match_dashboard()