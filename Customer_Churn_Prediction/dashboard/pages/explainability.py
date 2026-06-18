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

#=========================================
# COEFFICIENT TABLES
#=========================================
positive_coef_df = pd.DataFrame({
    "Feature":[
        "Fiber Optic",
        "Loyal Customer",
        "Streaming TV",
        "Streaming Movies",
        "Multiple Lines"
    ],
    "Coefficient":[0.789,0.414,0.236,0.234,0.213]
})
negative_coef_df = pd.DataFrame({
    "Feature":[
        "Tenure",
        "Monthly Charges",
        "Two Year Contract",
        "One Year Contract",
        "Online Security"
    ],
    "Coefficient":[-1.135,-0.893,-0.636,-0.294,-0.141]
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

for fig in [churn_fig, retention_fig]:
    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=500,
        font=dict(size=13)
    )
    fig.update_traces(textposition="outside")

def create_xai_card(title, value, color, icon):
    return dbc.Card(
        dbc.CardBody([
            html.Div(icon, className="kpi-icon"),
            html.H6(title,className="kpi-label"),
            html.H3(value,className=f"text-{color} fw-bold")
        ]),
        className="kpi-card"
    )
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
    # =====================================
    # PAGE BANNER
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Explainable AI & Churn Drivers",className="text-white fw-bold text-center"
            ),
            html.P(
                "Understand which customer attributes increase churn risk and which factors improve customer retention.",
                className="text-white text-center"
            )
        ]),
        className="overview-banner mb-4"
    ),
    # =====================================
    # OBJECTIVE
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H4("Analysis Objective",className="fw-bold"),
            html.P(
                "Use Logistic Regression coefficients to explain customer churn behavior and provide actionable business recommendations."
            )
        ]),
        className="shadow-sm mb-4"
    ),
    # =====================================
    # KPI CARDS
    # =====================================
    dbc.Row([
        dbc.Col(
            create_xai_card(
                "Top Churn Driver",
                "Fiber Optic",
                "danger",
                "⚠️"
            ),
            md=4
        ),
        dbc.Col(
            create_xai_card(
                "Top Retention Driver",
                "Tenure",
                "success",
                "🛡️"
            ),
            md=4
        ),
        dbc.Col(
            create_xai_card(
                "Model Type",
                "Logistic Regression",
                "primary",
                "🤖"
            ),
            md=4
        )
    ], className="mb-4"),
    # =====================================
    # DRIVER CHARTS
    # =====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(
                        "Top Churn Drivers",
                        className="fw-bold mb-0"
                    )
                ),
                dbc.CardBody([
                    dcc.Graph(
                        figure=churn_fig,
                        config={"displayModeBar": False}
                    )
                ])
            ]),
            md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(
                        "Top Retention Drivers",
                        className="fw-bold mb-0"
                    )
                ),
                dbc.CardBody([
                    dcc.Graph(
                        figure=retention_fig,
                        config={"displayModeBar": False}
                    )
                ])
            ]),
            md=6
        )
    ]),
    html.Br(),
    # =====================================
    # INTERPRETATION
    # =====================================

    dbc.Alert([
            html.H4("Model Interpretation",className="fw-bold"),
            html.Hr(),
            html.Ul([
                html.Li(
                    "Fiber Optic customers are significantly more likely to churn."
                ),
                html.Li(
                    "Customers with longer tenure are much more likely to remain loyal."
                ),
                html.Li(
                    "Two-year contracts strongly reduce churn risk."
                ),
                html.Li(
                    "Streaming services contribute slightly to churn probability."
                ),
                html.Li(
                    "Security and support services improve retention."
                )
            ])
        ],
        color="info",
        className="shadow-sm mb-4"
    ),
    html.Br(),
    # =====================================
    # COEFFICIENT TABLES
    # =====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(
                        "Top Positive Coefficients (Increase Churn)",   className="fw-bold mb-0"
                    )
                ),
                dbc.CardBody([
                    dbc.Table.from_dataframe(
                        positive_coef_df.round(3),
                        striped=True,
                        bordered=True,
                        hover=True,
                        responsive=True
                    )
                ])
            ]),md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(
                        "Top Negative Coefficients (Improve Retention)  ",className="fw-bold mb-0"
                    )
                ),
                dbc.CardBody([
                    dbc.Table.from_dataframe(
                        negative_coef_df.round(3),
                        striped=True,
                        bordered=True,
                        hover=True,
                        responsive=True
                    )
                ])
            ]),md=6
        )
    ]),
    html.Br(),
    dbc.Card(
        dbc.CardBody([
            html.H4("How To Interpret Coefficients",    className="fw-bold"),
            html.Hr(),
            html.P(
                """
                Positive coefficients increase the probability of   customer churn.
                Negative coefficients decrease churn probability and    improve customer retention.
                Larger absolute values indicate stronger influence on   the prediction.
                """
            )
        ]),
        className="shadow-sm mb-4"
    ),
    # =====================================
    # BUSINESS RECOMMENDATIONS
    # =====================================
    dbc.Card([
        dbc.CardHeader(
            html.H4("Business Recommendations",className="fw-bold mb-0")
        ),
        dbc.CardBody([
            html.Ul([html.Li(item)for item in recommendations])
        ])
    ],
    className="shadow-sm mb-4"),
    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    dbc.Alert([
            html.H4("Executive Summary",className="fw-bold"),
            html.Hr(),
            html.Ul([
                html.Li(
                    "Fiber Optic service is the strongest churn    indicator."
                ),
                html.Li(
                    "Customer tenure is the strongest retention factor. "
                ),
                html.Li(
                    "Long-term contracts significantly reduce churn risk."
                ),
                html.Li(
                    "Security-related services contribute positively to retention."
                ),
                html.Li(
                    "Retention programs should focus on new customers and month-to-month subscribers."
                )
            ])
        ],
        color="success",
        className="shadow-sm"
    )
], fluid=True)
