import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

from utils.data_loader import last_date

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/processed/covid_ML_dataset.csv")

latest_country_data = (
    df.sort_values("date")
      .groupby("location")
      .tail(1)
)

total_cases = int(latest_country_data["total_cases"].sum())
total_deaths = int(latest_country_data["total_deaths"].sum())

avg_vaccination = round(df['vaccination_rate'].mean(),2)
avg_mortality = round(df['mortality_rate'].mean(),2)

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
                    DashIconify(
                        icon="mdi:virus",
                        width=40
                    ),
                    html.H5("Total Cases"),
                    html.H3(f"{total_cases:,}")
                ]),
                color="primary",
                inverse=True
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(
                        icon="mdi:skull",
                        width=40
                    ),
                    html.H5("Total Deaths"),
                    html.H3(f"{total_deaths:,}")
                ]),
                color="danger",
                inverse=True
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(
                        icon="mdi:syringe",
                        width=40
                    ),
                    html.H5("Avg Vaccination Rate"),
                    html.H3(f"{avg_vaccination:.2f}%")
                ]),
                color="success",
                inverse=True
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    DashIconify(
                        icon="mdi:heart-pulse",
                        width=40
                    ),
                    html.H5("Avg Mortality Rate"),
                    html.H3(f"{avg_mortality:.2f}%")
                ]),
                color="warning",
                inverse=True
            ),
            width=3
        ),
    ],
    className="g-4"
    )
], fluid=True)
