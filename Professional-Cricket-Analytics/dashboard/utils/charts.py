from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import (
    BACKGROUND_COLOR,
    BORDER_COLOR,
    MUTED_TEXT_COLOR,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    TEXT_COLOR,
)

# ==========================================================
# Common chart configuration
# ==========================================================
DEFAULT_CHART_HEIGHT = 450
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
    ],
}

# ==========================================================
# Column validation
# ==========================================================
def validate_chart_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str]
) -> None:
    """
    Validate that all columns required by a chart exist.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Data used to create the chart.

    required_columns : list[str]
        Columns required for the chart.

    Raises
    ------
    KeyError
        If any required column is missing.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Chart data is missing required columns: "
            f"{missing_columns}"
        )

# ==========================================================
# Common chart styling
# ==========================================================
def apply_common_layout(
    figure: go.Figure,
    title: Optional[str] = None,
    x_axis_title: Optional[str] = None,
    y_axis_title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    show_legend: bool = False
) -> go.Figure:
    """
    Apply common dark-theme layout settings to a Plotly figure.
    """

    figure.update_layout(
        title={
            "text": title or "",
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 20,
                "color": TEXT_COLOR,
            },
        },
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        height=height,
        showlegend=show_legend,
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        margin={
            "l": 50,
            "r": 35,
            "t": 75,
            "b": 60,
        },
        hovermode="closest",
        font={
            "family": "Arial, sans-serif",
            "size": 13,
            "color": TEXT_COLOR,
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {
                "color": TEXT_COLOR,
            },
        },
        hoverlabel={
            "bgcolor": "#111722",
            "bordercolor": BORDER_COLOR,
            "font": {
                "color": TEXT_COLOR,
            },
        },
    )

    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
        automargin=True,
        linecolor=BORDER_COLOR,
        tickcolor=BORDER_COLOR,
        tickfont={
            "color": MUTED_TEXT_COLOR,
        },
        title_font={
            "color": TEXT_COLOR,
        },
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(170, 178, 192, 0.12)",
        zeroline=False,
        automargin=True,
        linecolor=BORDER_COLOR,
        tickcolor=BORDER_COLOR,
        tickfont={
            "color": MUTED_TEXT_COLOR,
        },
        title_font={
            "color": TEXT_COLOR,
        },
    )

    return figure

# ==========================================================
# Empty chart
# ==========================================================
def create_empty_chart(
    message: str = "No data available for the selected filters.",
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT
) -> go.Figure:
    """
    Create a placeholder figure when filtered data is empty.
    """

    figure = go.Figure()

    figure.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={
            "size": 16,
        },
    )

    figure.update_xaxes(
        visible=False
    )

    figure.update_yaxes(
        visible=False
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        height=height,
        show_legend=False,
    )

# ==========================================================
# Vertical bar chart
# ==========================================================
def create_bar_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_axis_title: Optional[str] = None,
    y_axis_title: Optional[str] = None,
    color_column: Optional[str] = None,
    text_column: Optional[str] = None,
    sort_by: Optional[str] = None,
    ascending: bool = False,
    height: int = DEFAULT_CHART_HEIGHT,
    show_legend: bool = False
) -> go.Figure:
    """
    Create a reusable vertical bar chart.
    """

    required_columns = [
        x_column,
        y_column,
    ]

    if color_column is not None:
        required_columns.append(color_column)

    if text_column is not None:
        required_columns.append(text_column)

    validate_chart_columns(
        dataframe,
        required_columns
    )

    if dataframe.empty:
        return create_empty_chart(
            title=title,
            height=height
        )

    chart_df = dataframe.copy()

    if sort_by is not None:
        validate_chart_columns(
            chart_df,
            [sort_by]
        )

        chart_df = chart_df.sort_values(
            by=sort_by,
            ascending=ascending
        )

    figure = px.bar(
        chart_df,
        x=x_column,
        y=y_column,
        color=color_column,
        text=text_column,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
        ],
    )

    figure.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            f"<b>%{{x}}</b><br>"
            f"{y_axis_title or y_column}: %{{y:,}}"
            "<extra></extra>"
        ),
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        x_axis_title=x_axis_title,
        y_axis_title=y_axis_title,
        height=height,
        show_legend=show_legend,
    )

# ==========================================================
# Horizontal bar chart
# ==========================================================
def create_horizontal_bar_chart(
    dataframe: pd.DataFrame,
    category_column: str,
    value_column: str,
    title: str,
    x_axis_title: Optional[str] = None,
    y_axis_title: Optional[str] = None,
    top_n: Optional[int] = None,
    ascending: bool = True,
    height: int = DEFAULT_CHART_HEIGHT
) -> go.Figure:
    """
    Create a horizontal ranking chart.
    """

    validate_chart_columns(
        dataframe,
        [
            category_column,
            value_column,
        ]
    )

    if dataframe.empty:
        return create_empty_chart(
            title=title,
            height=height
        )

    chart_df = dataframe.copy()

    chart_df = chart_df.sort_values(
        by=value_column,
        ascending=False
    )

    if top_n is not None:
        chart_df = chart_df.head(top_n)

    chart_df = chart_df.sort_values(
        by=value_column,
        ascending=ascending
    )

    figure = px.bar(
        chart_df,
        x=value_column,
        y=category_column,
        orientation="h",
        text=value_column,
        color_discrete_sequence=[
            PRIMARY_COLOR
        ],
    )

    figure.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            f"<b>%{{y}}</b><br>"
            f"{x_axis_title or value_column}: %{{x:,}}"
            "<extra></extra>"
        ),
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        x_axis_title=x_axis_title,
        y_axis_title=y_axis_title,
        height=height,
        show_legend=False,
    )

# ==========================================================
# Line chart
# ==========================================================
def create_line_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_axis_title: Optional[str] = None,
    y_axis_title: Optional[str] = None,
    color_column: Optional[str] = None,
    markers: bool = True,
    height: int = DEFAULT_CHART_HEIGHT,
    show_legend: bool = False
) -> go.Figure:
    """
    Create a reusable line chart.
    """

    required_columns = [
        x_column,
        y_column,
    ]

    if color_column is not None:
        required_columns.append(color_column)

    validate_chart_columns(
        dataframe,
        required_columns
    )

    if dataframe.empty:
        return create_empty_chart(
            title=title,
            height=height
        )

    chart_df = dataframe.copy()

    chart_df = chart_df.sort_values(
        by=x_column
    )

    figure = px.line(
        chart_df,
        x=x_column,
        y=y_column,
        color=color_column,
        markers=markers,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
        ],
    )

    figure.update_traces(
        hovertemplate=(
            f"<b>%{{x}}</b><br>"
            f"{y_axis_title or y_column}: %{{y:,.2f}}"
            "<extra></extra>"
        )
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        x_axis_title=x_axis_title,
        y_axis_title=y_axis_title,
        height=height,
        show_legend=show_legend,
    )

# ==========================================================
# Pie or donut chart
# ==========================================================
def create_pie_chart(
    dataframe: pd.DataFrame,
    names_column: str,
    values_column: str,
    title: str,
    hole: float = 0.45,
    height: int = DEFAULT_CHART_HEIGHT
) -> go.Figure:
    """
    Create a reusable pie or donut chart.

    A hole value of 0 creates a normal pie chart.
    A value greater than 0 creates a donut chart.
    """

    validate_chart_columns(
        dataframe,
        [
            names_column,
            values_column,
        ]
    )

    if dataframe.empty:
        return create_empty_chart(
            title=title,
            height=height
        )

    figure = px.pie(
        dataframe,
        names=names_column,
        values=values_column,
        hole=hole,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            "#2CA02C",
            "#D62728",
            "#9467BD",
            "#8C564B",
        ],
    )

    figure.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{value:,}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        ),
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        height=height,
        show_legend=True,
    )

# ==========================================================
# Scatter chart
# ==========================================================
def create_scatter_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_axis_title: Optional[str] = None,
    y_axis_title: Optional[str] = None,
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    hover_name: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    show_legend: bool = True
) -> go.Figure:
    """
    Create a reusable scatter chart.
    """

    required_columns = [
        x_column,
        y_column,
    ]

    for optional_column in [
        color_column,
        size_column,
        hover_name,
    ]:
        if optional_column is not None:
            required_columns.append(
                optional_column
            )

    validate_chart_columns(
        dataframe,
        required_columns
    )

    if dataframe.empty:
        return create_empty_chart(
            title=title,
            height=height
        )

    figure = px.scatter(
        dataframe,
        x=x_column,
        y=y_column,
        color=color_column,
        size=size_column,
        hover_name=hover_name,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
        ],
    )

    figure.update_traces(
        marker={
            "opacity": 0.8,
            "line": {
                "width": 0.5,
            },
        }
    )

    return apply_common_layout(
        figure=figure,
        title=title,
        x_axis_title=x_axis_title,
        y_axis_title=y_axis_title,
        height=height,
        show_legend=show_legend,
    )

