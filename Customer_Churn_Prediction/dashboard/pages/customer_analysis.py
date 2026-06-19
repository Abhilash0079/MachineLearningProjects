import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dashboard.utils.data_loader import load_data

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

for fig in [contract_fig,internet_fig,payment_fig,tenure_fig]:
    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13)
    )
    fig.update_traces(textposition="outside")
#=====================================
# LAYOUT
#=====================================
customer_analyis_layout = dbc.Container([
    # =====================================
    # PAGE BANNER
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Customer Segmentation & Churn Analysis",
                className="text-white fw-bold text-center"
            ),
            html.P(
                "Understand which customer groups are most likely to churn and identify retention opportunities.",
                className="text-white text-center"
            )
        ]),
        className="overview-banner mb-4"
    ),
    # =====================================
    # BUSINESS OBJECTIVE
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H4("Analysis Objective",className="fw-bold"),
            html.P(
                "Analyze customer characteristics, contract types, internet services, payment methods and tenure patterns to uncover drivers of customer churn."
            )
        ]),
        className="shadow-sm mb-4"
    ),
    # =====================================
    # ROW 1
    # =====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Contract Type Analysis"),
                dbc.CardBody([
                    dcc.Graph(figure=contract_fig,config={"displayModeBar": False})
                ])
            ]),
            md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Internet Service Analysis"),
                dbc.CardBody([
                    dcc.Graph(figure=internet_fig,config={"displayModeBar": False})
                ])
            ]),
            md=6
        )
    ]),
    html.Br(),
    # =====================================
    # ROW 2
    # =====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Payment Method Analysis"),
                dbc.CardBody([
                    dcc.Graph(figure=payment_fig,
                        config={"displayModeBar": False})
                ])
            ]),
            md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Tenure Group Analysis"),
                dbc.CardBody([
                    dcc.Graph(figure=tenure_fig,
                        config={"displayModeBar": False})
                ])
            ]),
            md=6
        )
    ]),
    html.Br(),
    # =====================================
    # EXECUTIVE INSIGHTS
    # =====================================
    dbc.Alert([
            html.H4("Executive Insights",className="fw-bold"),
            html.Hr(),
            html.Ul([
                html.Li(
                    "Month-to-month contract customers exhibit the highest churn behavior."
                ),
                html.Li(
                    "Electronic check users are significantly more likely to churn."
                ),
                html.Li(
                    "Customers with shorter tenure have substantially higher churn rates."
                ),
                html.Li(
                    "Long-term customers demonstrate strong loyalty and retention."
                ),
                html.Li(
                    "Fiber optic customers show higher churn compared to other internet services."
                )
            ])
        ],
        color="info",
        className="shadow-sm mb-4"
    ),
    # =====================================
    # RECOMMENDATIONS
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H4("Business Recommendations",className="fw-bold text-success"
            ),
            html.Hr(),
            html.Ul([
                html.Li(
                    "Promote annual and two-year contracts to reduce churn."
                ),
                html.Li(
                    "Introduce retention campaigns for customers within their first year."
                ),
                html.Li(
                    "Provide incentives for automatic payment enrollment."
                ),
                html.Li(
                    "Focus customer success efforts on high-risk Fiber Optic customers."
                ),
                html.Li(
                    "Offer personalized discounts to newly acquired customers."
                )
            ])
        ]),
        className="shadow-sm"
    )
], fluid=True)