import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dashboard.utils.data_loader import load_data

#====================================
# LOAD DATA
#====================================
df = load_data()
#====================================
# KPIs
#====================================
total_customers = len(df)
churned_customers = (df['Churn']==1).sum()
churn_rate = (churned_customers/total_customers)*100
avg_monthly = df['MonthlyCharges'].mean()
avg_tenure = df['tenure'].mean()

#====================================
# CHURN DISTRIBUTION
#====================================
churn_df = df['Churn'].value_counts().reset_index()
churn_df.columns = ['Status', 'Count']
churn_df['Status'] = churn_df['Status'].map({
    0:'Stayed',
    1:'Churned'
})

pie_fig = px.pie(
    churn_df, 
    names="Status", 
    values='Count', 
    title="Customer Churn Distribution"
)
pie_fig.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=14),
    legend=dict(orientation="h",y=-0.1)
)

#====================================
# TENURE DISTRIBUTION
#====================================
tenure_fig = px.histogram(
    df,
    x='tenure',
    nbins=30,
    title="Customer Tenure Distribution"
)

tenure_fig.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    height=450
)

#====================================
# KPI CARD
#====================================
def create_card(title, value, color, icon="📊"):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                    html.Div(icon, className="kpi-icon"),
                    html.H6(title, className="kpi-label"),
                    html.H2(value, className="kpi-value")
                ],
                className="text-center"
            )
        ]),
        className=f"kpi-card border-start border-5 border-{color}"
    )

#====================================
# LAYOUT
#====================================
overview_layout = dbc.Container([
    # ====================================
    # HERO SECTION
    # ====================================
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Customer Churn Intelligence Dashboard",
                className="text-white fw-bold text-center"
            ),
            html.P(
                "Analyze customer behavior, monitor churn trends and identify retention opportunities.",
                className="text-white text-center"
            )
        ]),
        className="overview-banner mb-4"
    ),
    # ====================================
    # KPI SECTION
    # ====================================
    dbc.Row([
        dbc.Col(
            create_card(
                "Total Customers",
                f"{total_customers}", "primary", "👥"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Churned Customers",
                f"{churned_customers}", "danger","⚠️"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Churn Rate",
                f"{churn_rate:.2f}%", "warning","📉"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Avg Tenure",
                f"{avg_tenure:.1f} Months", "success","⏳"
            ),
            md=3
        )
    ], className="mb-4"),
    html.Br(),
    # ====================================
    # BUSINESS OBJECTIVE
    # ====================================
    dbc.Card(
        dbc.CardBody([
            html.H4("Business Objective",className="fw-bold"),
            html.P(
                "The goal of this platform is to identify customers at risk of churn and provide actionable insights to improve retention and customer lifetime value."
            )
        ]),
        className="mb-4 shadow-sm"
    ),
    # ====================================
    # VISUALIZATIONS
    # ====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Customer Churn Distribution",className="fw-bold"
                    )
                ),
                dbc.CardBody([
                    dcc.Graph(figure=pie_fig, 
                              config={"displayModeBar":False})
                ])
            ]),
            md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(
                        "Customer Tenure Distribution",
                        className="fw-bold"
                    )
                ),
                dbc.CardBody([
                    dcc.Graph(figure=tenure_fig)
                ])
            ]),
            md=6
        )
    ]),
    html.Br(),
    # ====================================
    # INSIGHTS
    # ====================================
    dbc.Alert(
        [
            html.H5("Executive Summary",className="fw-bold"),
            html.Hr(),
            html.Ul([
                html.Li(
                    f"Overall churn rate is {churn_rate:.1f}%."
                ),
                html.Li(
                    "Customers with shorter tenure are significantly more likely to churn."
                ),
                html.Li(
                    "Month-to-month contracts show the highest churn behavior."
                ),
                html.Li(
                    "Retention efforts should focus on newly acquired customers."
                )
            ])
        ],
        color="info", className="shadow-sm"
    )
], fluid=True)
