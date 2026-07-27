import streamlit as st
from utils.data_loader import load_all_data
from utils.executive_analytics import (calculate_executive_kpis,)
from utils.filters import (
    display_global_filters,
    filter_deliveries,
    filter_matches,
    get_filtered_match_ids,
)
from utils.helpers import (format_decimal, format_integer,)
from utils.page_components import (display_page_header,)


# ==========================================================
# Filter controls
# ==========================================================

def display_executive_filters(
    matches_df,
    deliveries_df,
) -> tuple[dict, object, object]:
    """
    Display permanent Executive Dashboard filters and apply them.
    """

    st.subheader("🔎 Dashboard Filters")

    selected_filters = display_global_filters(
        matches_df=matches_df,
        deliveries_df=deliveries_df,
        include_player_filters=False,
        key_prefix="executive",
    )

    filtered_matches_df = filter_matches(
        matches_df=matches_df,
        season=selected_filters["season"],
        team=selected_filters["team"],
        venue=selected_filters["venue"],
    )

    filtered_match_ids = get_filtered_match_ids(
        filtered_matches_df
    )

    filtered_deliveries_df = filter_deliveries(
        deliveries_df=deliveries_df,
        match_ids=filtered_match_ids,
        team=selected_filters["team"],
        batter="All",
        bowler="All",
    )

    return (
        selected_filters,
        filtered_matches_df,
        filtered_deliveries_df,
    )


# ==========================================================
# Filter summary
# ==========================================================

def display_filter_summary(
    selected_filters: dict,
) -> None:
    """
    Display a concise summary of active filters.
    """

    season = selected_filters.get(
        "season",
        "All",
    )

    team = selected_filters.get(
        "team",
        "All",
    )

    venue = selected_filters.get(
        "venue",
        "All",
    )

    st.caption(
        f"Active selection — "
        f"Season: {season} | "
        f"Team: {team} | "
        f"Venue: {venue}"
    )


# ==========================================================
# KPI cards
# ==========================================================

def display_executive_kpis(
    filtered_matches_df,
    filtered_deliveries_df,
) -> None:
    """
    Display league-level KPI cards.
    """

    kpis = calculate_executive_kpis(
        matches_df=filtered_matches_df,
        deliveries_df=filtered_deliveries_df,
    )

    st.subheader("📌 League Overview")

    first_row = st.columns(4)

    first_row[0].metric(
        label="Matches",
        value=format_integer(
            kpis["total_matches"]
        ),
    )

    first_row[1].metric(
        label="Total Runs",
        value=format_integer(
            kpis["total_runs"]
        ),
    )

    first_row[2].metric(
        label="Wickets",
        value=format_integer(
            kpis["total_wickets"]
        ),
    )

    first_row[3].metric(
        label="Participating Teams",
        value=format_integer(
            kpis["participating_teams"]
        ),
    )

    second_row = st.columns(3)

    second_row[0].metric(
        label="Completed Matches",
        value=format_integer(
            kpis["completed_matches"]
        ),
    )

    second_row[1].metric(
        label="Runs per Match",
        value=format_decimal(
            kpis["average_runs_per_match"],
            decimal_places=1,
        ),
    )

    second_row[2].metric(
        label="Wickets per Match",
        value=format_decimal(
            kpis["average_wickets_per_match"],
            decimal_places=1,
        ),
    )


# ==========================================================
# Main page
# ==========================================================

def show_executive_dashboard() -> None:
    """
    Display the Executive Dashboard.
    """

    display_page_header(
        title="Executive Dashboard",
        subtitle=(
            "League-level performance, competition trends "
            "and strategic cricket intelligence."
        ),
        icon="📈",
    )

    try:
        data = load_all_data()

        matches_df = data["matches"]
        deliveries_df = data["deliveries"]

        (
            selected_filters,
            filtered_matches_df,
            filtered_deliveries_df,
        ) = display_executive_filters(
            matches_df=matches_df,
            deliveries_df=deliveries_df,
        )

        display_filter_summary(
            selected_filters
        )

        if filtered_matches_df.empty:

            st.warning(
                "No matches are available for the selected "
                "combination of filters."
            )

            st.stop()

        display_executive_kpis(
            filtered_matches_df=filtered_matches_df,
            filtered_deliveries_df=filtered_deliveries_df,
        )

        st.info(
            "Executive charts will be added after the filter "
            "and KPI section has been verified."
        )

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        TypeError,
        RuntimeError,
    ) as error:

        st.error(
            f"Executive Dashboard could not be loaded: {error}"
        )


show_executive_dashboard()