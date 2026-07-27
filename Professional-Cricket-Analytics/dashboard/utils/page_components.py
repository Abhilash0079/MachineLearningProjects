import streamlit as st

from utils.helpers import create_page_header


def display_page_header(
    title: str,
    subtitle: str,
    icon: str
) -> None:
    """
    Display a standard CricVision AI dashboard page header.

    Parameters
    ----------
    title : str
        Page title.

    subtitle : str
        Short explanation of the page.

    icon : str
        Emoji or icon displayed with the title.
    """

    st.html(
        create_page_header(
            title=title,
            subtitle=subtitle,
            icon=icon,
        )
    )


def display_development_notice(
    message: str = (
        "This dashboard page has been created successfully. "
        "Analytics components will be added in the next steps."
    )
) -> None:
    """
    Display a temporary development notice.
    """

    st.info(message)


def display_dashboard_scope(
    features: list[str]
) -> None:
    """
    Display the planned analytical scope of a dashboard page.

    Parameters
    ----------
    features : list[str]
        Planned dashboard capabilities.
    """

    st.subheader("Dashboard Scope")

    for feature in features:
        st.markdown(
            f"- {feature}"
        )