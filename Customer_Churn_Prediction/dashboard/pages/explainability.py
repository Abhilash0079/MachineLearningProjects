import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

#==========================
# CHURN FACTORS
#==========================
churn_df = pd.DataFrame({
    "Feature":[
        "Fiber Optic",
        "Loyal Customer",
        "Streaming TV",
        "Streaming Movies",
        "Multiple Lines"
    ],
    "Impact":[0.789,0.414,0.236,0.234,0.213]
})

#==========================
# CHURN DRIVE CHART
#==========================
churn_fig = px.bar(
    churn_df,
    x='Impact',
    y='Feature',
    orientation='h',
    title="Top Churn Drivers",
    text_auto=".3f",
    color="Impact"
)
churn_fig.update_layout(template='plotly_white', height=500)

#==========================
# RETENTION FACTORS
#==========================
retention_df = pd.DataFrame({
    "Feature":[
        "Tenure",
        "Monthly Charges",
        "Two Year Contract",
        "One Year Contract",
        "Online Security"
    ],
    "Impact":[-1.135,-0.893,-0.636,-0.294,-0.141]
})

#==========================
# RETENTION DRIVE CHART
#==========================
retention_fig = px.bar(
    retention_df,
    x='Impact',
    y='Feature',
    orientation='h',
    title="Top Retention Drivers",
    text_auto=".3f",
    color="Impact"
)
retention_fig.update_layout(template='plotly_white', height=500)

#============================
# BUSINESS RECOMMENDATIONS
#============================
recommendations = [
    "Promote long-term contracts through discounts and loyalty rewards.",
    "Encourage adoption of Online Security and Tech Support services.",
    "Create targeted retention campaigns for Fiber Optic customers.",
    "Monitor customers with month-to-month contracts for churn risk.",
    "Offer personalized retention incentives to new customers."
]

#=====================
# LAYOUT
#=====================
explainability_layout = dbc.Container([
    html.Br(),
    html.H2("Explainable AI Dashboard", className="text-center fw-bold text-primary"),
    html.Hr(),
    dbc.Alert([
        html.B("Objective: "),
        "Understand which factors increase or decrease customer churn."
    ], color="info"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Churn Drivers"),
                dbc.CardBody([dcc.Graph(figure=churn_fig)])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Rentention Drivers"),
                dbc.CardBody([dcc.Graph(figure=retention_fig)])
            ]),
            width=6
        )
    ]),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H4("Business Recommendation: ")),
        dbc.CardBody([
            html.Ul([
                html.Li(item) for item in recommendations
            ])
        ])
    ]),
    html.Br(),
    dbc.Alert([
        html.B("Executive Summary: "),
        "Contract type, tenure, internet service and security-related services are the strongest drivers of customer churn. Long-term contracts significantly improve retention."
    ],color='success')
], fluid=True)
