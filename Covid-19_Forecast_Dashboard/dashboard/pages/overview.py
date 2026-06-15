import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

from utils.data_loader import load_india_data

# ==========================================
# LOAD DATA
# ==========================================

df = load_india_data()
df['date'] = pd.to_datetime(df['date'])

# =====================================================
# LATEST RECORD
# =====================================================

last_valid_row = df[df["total_cases"] > 0].iloc[-1]
total_cases = int(last_valid_row["total_cases"])
total_deaths = int(last_valid_row["total_deaths"])
new_cases = int(last_valid_row['new_cases'])
vaccination_rate = round(df['vaccination_rate'].iloc[-1],2)
mortality_rate = round((total_deaths /total_cases) * 100,2)
last_date = pd.to_datetime(last_valid_row["date"]).strftime("%d %B %Y")

# ==========================================
# LAYOUT
# ==========================================

overview_layout = dbc.Container([
    html.H5(
        f"Last Updated: {last_date}",
        className="text-muted text-center mb-4 fw-bold text-secondary"
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(icon="mdi:virus", width=40),
                    html.H5("Total Cases",className="mt-2"),
                    html.H4(f"{total_cases:,}", className="fw-bold", style={'color':'#ffffff'})
                ]),
                color="primary",
                inverse=True,
                className="card"
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(icon="mdi:skull",width=40),
                    html.H5("Total Deaths",className="mt-2"),
                    html.H4(f"{total_deaths:,}", className="fw-bold", style={'color':'#ffffff'})
                ]),
                color="danger",
                inverse=True,
                className="card"
            ),
            width=2
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(icon="mdi:chart-line",width=40),
                    html.H5("New Cases",className="mt-2"),
                    html.H4(f"{new_cases:,}", className="fw-bold", style={'color':'#ffffff'})
                ]),
                color="info",
                inverse=True,
                className="card"
            ),
            width=2
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(icon="mdi:syringe",width=40),
                    html.H5("Vaccination Rate", className="mt-2"),
                    html.H4(f"{vaccination_rate:.2f}%", className="fw-bold", style={'color':'#ffffff'})
                ]),
                color="success",
                inverse=True,
                className="card"
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(icon="mdi:heart-pulse",width=40),
                    html.H5("Mortality Rate", className="mt-2"),
                    html.H4(f"{mortality_rate:.2f}%", className="fw-bold", style={'color':'#ffffff'})
                ]),
                color="warning",
                inverse=True,
                className="card"
            ),
            width=2
        ),
    ],
    className="mb-4"
    ),
    html.H3("Project Summary"),
    html.P("""
            This dashboard analyzes COVID-19 trends in India using machine learning and interactive visualizations.

            The forecasting model uses XGBoost with lag-based features to predict future case counts.
            """
        )
], fluid=True)
