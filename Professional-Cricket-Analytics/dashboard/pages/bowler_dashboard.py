import streamlit as st

from utils.page_components import (
    display_dashboard_scope,
    display_development_notice,
    display_page_header,
)


def show_bowler_dashboard() -> None:
    """
    Display the Bowler Dashboard page.
    """

    display_page_header(
        title="Bowler Dashboard",
        subtitle=(
            "Analyse wickets, economy, strike rate, "
            "bowling phases and dismissal effectiveness."
        ),
        icon="🎯",
    )

    display_development_notice()

    display_dashboard_scope(
        features=[
            "Wickets and innings summary",
            "Bowling average",
            "Economy rate",
            "Bowling strike rate",
            "Season-wise wicket trend",
            "Powerplay, middle-over and death-over performance",
            "Dismissal-type analysis",
            "Venue and opposition performance",
        ]
    )


show_bowler_dashboard()