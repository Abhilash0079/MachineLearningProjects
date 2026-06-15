import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.data_loader import load_india_data

#===========================================
# LOAD DATA
#===========================================

df = load_india_data()
df['date'] = pd.to_datetime(df['date'])

#===========================================
# KPI METRICES
#===========================================

latest_vaccination_rate = round(df['vaccination_rate'].max(),2)
total_vaccinated = int(df['people_vaccinated'].max())
peak_coverage = round(df['vaccination_rate'].max(),2)

#===========================================
# VACCINATED PEOPLE TREND
#===========================================

vaccinated_fig = px.line(
    df,
    x='date',
    y='people_vaccinated',
    title="People Vaccinated Over Time"
)
vaccinated_fig.update_layout(
    template='plotly_white',
    xaxis_rangeslider_visible=True,
    height=500
)

#===========================================
# VACCINATION RATE TREND
#===========================================

vaccination_rate_fig = px.line(
    df,
    x='date',
    y='vaccination_rate',
    title="Vaccinated Rate Growth (%)"
)

vaccination_rate_fig.update_layout(
    template='plotly_white',
    xaxis_rangeslider_visible=True,
    height=500
)

#===========================================
# CASES VS VACCINATION
#===========================================

scatter_fig = px.scatter(
    df,
    x="vaccination_rate",
    y="cases_7d_avg",
    title="Cases vs Vaccination Rate",
    opacity=0.7
)

scatter_fig.update_layout(
    template="plotly_white",
    height=500
)

#===========================================
# PAGE LAYOUT
#===========================================

vaccination_layout = dbc.Container([
    html.Br(),
    html.H2("India Vaccination Analysis", className="text-center text-success fw-bold"),
    html.Hr(),
    #===========================================
    # KPI CARDS
    #===========================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("People Vaccinated"),
                    html.H3(f"{total_vaccinated:,}")
                ])
            ],
            color="primary",
            inverse=True
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Vaccination Rate"),
                    html.H3(f"{latest_vaccination_rate}%")
                ])
            ],
            color="success",
            inverse=True),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Peak Coverage"),
                    html.H3(f"{peak_coverage}%")
                ])
            ],
            color="info",
            inverse=True),
            width=4
        )
    ], className="mb-4"),
    # =================================================
    # INSIGHT ALERT
    # =================================================
    dbc.Alert([
        html.B("Key Insight: "),
        "India achieved more than 72% vaccination coverage. "
        "Following mass vaccination campaigns, major COVID-19 waves became less severe compared to the second wave of 2021."
    ],
    color="success",
    className="mb-4"
    ),
    # =================================================
    # CHARTS
    # =================================================
    dbc.Card([
        dbc.CardHeader("Vaccinated Population Growth"),
        dbc.CardBody([dcc.Graph(figure=vaccinated_fig)])
    ],
    className="mb-4"),
    dbc.Card([
        dbc.CardHeader("Vaccination Rate Trend"),
        dbc.CardBody([dcc.Graph(figure=vaccination_rate_fig)])
    ],
    className="mb-4"),
    dbc.Card([
        dbc.CardHeader("Cases vs Vaccination Relationship"),
        dbc.CardBody([dcc.Graph(figure=scatter_fig)])
    ])
],fluid=True)
