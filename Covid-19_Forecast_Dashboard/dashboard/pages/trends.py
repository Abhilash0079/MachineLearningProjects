import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.data_loader import load_india_data

#=======================================
# LOAD DATA
#=======================================

df = load_india_data()
df['date'] = pd.to_datetime(df['date'])

#========================================
# DATE SLIDER
#========================================
date_slider = html.Div([
    html.H4(
        "Select Date Range"
    ),
    dcc.DatePickerRange(
        id='date-range',
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format="DD MMM YYYY"
    )
], className="text-center mb-4 fw-bold text-secondary")

# =====================================================
# PEAK WAVE ANALYSIS
# =====================================================

peak_row = df.loc[df["cases_7d_avg"].idxmax()]
peak_date = pd.to_datetime(peak_row["date"]).strftime("%d %B %Y")
peak_cases = int(peak_row["cases_7d_avg"])

# =====================================================
# CASES TREND
# =====================================================

cases_fig = px.line(
    df,
    x="date",
    y="cases_7d_avg",
    title="7-Day Average COVID-19 Cases in India"
)

cases_fig.update_layout(
    template="plotly_white",
    # xaxis_rangeslider_visible=True,
    height=500
)

cases_fig.update_yaxes(title="Average Daily Cases")

# =====================================================
# MOVING AVERAGE COMPARISON
# =====================================================

ma_fig = px.line(
    df,
    x="date",
    y=["cases_7d_avg","cases_14d_avg"],
    title="7-Day vs 14-Day Moving Average"
)

ma_fig.update_layout(
    template="plotly_white",
    # xaxis_rangeslider_visible=True,
    height=500
)

ma_fig.update_traces(
    selector=dict(name="cases_7d_avg"),
    name="7-Day Average"
)

ma_fig.update_traces(
    selector=dict(name="cases_14d_avg"),
    name="14-Day Average"
)

# =====================================================
# DAILY DEATHS TREND
# =====================================================

death_fig = px.line(
    df,
    x="date",
    y="new_deaths",
    title="Daily COVID-19 Deaths in India"
)

death_fig.update_layout(
    template="plotly_white",
    # xaxis_rangeslider_visible=True,
    height=500
)

death_fig.update_yaxes(title="Daily Deaths")

# =====================================================
# PAGE LAYOUT
# =====================================================

trends_layout = dbc.Container([
    html.Br(),
    html.H2(
        "India COVID-19 Trend Analysis",
        className="text-center text-primary fw-bold"
    ),
    html.Hr(),
    # Peak Alert
    dbc.Alert(
        f"Peak COVID Wave: {peak_cases:,} average daily cases reported on {peak_date}",
        color="danger",
        className="mb-3"
    ),
    # Key Insight
    dbc.Alert(
        [
            html.B("Key Insight: "),
            "India experienced its most severe COVID-19 wave during April–May 2021. "
            "Case counts declined significantly after vaccination campaigns and public health interventions."
        ],
        color="info",
        className="mb-4"
    ),
    # Date Slider
    date_slider,
    html.Br(),
    # Cases Trend
    dbc.Card([
        dbc.CardHeader("Cases Trend"),
        dbc.CardBody([dcc.Graph(id='cases-trend')])
    ],
    className="mb-4"),
    # Moving Average Trend
    dbc.Card([
        dbc.CardHeader("Moving Average Comparison"),
        dbc.CardBody([dcc.Graph(id='ma-trend')])
    ],
    className="mb-4"),
    # Death Trend
    dbc.Card([
        dbc.CardHeader("Deaths Trend"),
        dbc.CardBody([dcc.Graph(id='deaths-trend')])
    ])
],
fluid=True)