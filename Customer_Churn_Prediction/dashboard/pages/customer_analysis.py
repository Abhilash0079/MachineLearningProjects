import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.data_loader import load_data

#=====================================
# LOAD DATA
#=====================================
df = load_data()

#=====================================
# 1. CHURN BY CONTRACT TYPE
#=====================================
contract_df = df.groupby("Contract")['Churn'].mean().reset_index()
contract_df['Churn']*=100

contract_fig = px.bar(
    contract_df,
    x='Contract',
    y='Churn',
    title="Churn Rate by Contract Type",
    text_auto=".1f"
)
contract_fig.update_layout(template='plotly_white')

"""
Insights: Month-to-month customers should have the highest churn.
"""

#=====================================
# 2. CHURN BY INTERNET SERVICE
#=====================================
internet_df = df.groupby('InternetService')['Churn'].mean().reset_index()
internet_df['Churn']*=100

internet_fig = px.bar(
    internet_df,
    x='InternetService',
    y='Churn',
    title="Churn Rate by Internet Service"
)
internet_fig.update_layout(template="plotly_white")

#=====================================
# 3. CHURN BY PAYMENT METHOD
#=====================================
payment_df = df.groupby("PaymentMethod")['Churn'].mean().reset_index()
payment_df['Churn']*=100

payment_fig = px.bar(
    payment_df,
    x='PaymentMethod',
    y='Churn',
    title="Churn Rate by Payment Method"
)
payment_fig.update_layout(template="plotly_white")

#=====================================
# 4. CHURN BY TENURE GROUP
#=====================================
tenure_df = df.groupby("TenureGroup")['Churn'].mean().reset_index()
tenure_df['Churn']*=100

tenure_fig = px.bar(
    tenure_df,
    x='TenureGroup',
    y='Churn',
    title="Churn Rate by Customer Tenure"
)
tenure_fig.update_layout(template="plotly_white")

#=====================================
# LAYOUT
#=====================================
customer_analyis_layout = dbc.Container([
    html.Br(),
    html.H2(
        "Customer Analysis",
        className="text-center fw-bold text-primary"
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=contract_fig)
                ])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=internet_fig)
                ])
            ]),
            width=6
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=payment_fig)
                ])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=tenure_fig)
                ])
            ]),
            width=6
        )
    ]),
    html.Br(),
    dbc.Alert([
        html.B("Key Business Insight: "),
        "Customers on month-to-month contracts and electronic check payments exhibit significantly higher churn rates. Longer tenure customers show much stronger retention."
    ],color='info')
], fluid=True)