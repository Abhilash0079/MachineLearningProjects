import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.data_loader import load_data

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

#====================================
# TENURE DISTRIBUTION
#====================================
tenure_fig = px.histogram(
    df,
    x='tenure',
    nbins=30,
    title="Customer Tenure Distribution"
)

tenure_fig.update_layout(template="plotly_white")

#====================================
# KPI CARD
#====================================
def create_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"),
            html.H3(value, className="fw-bold")
        ]),
        className=f"shadow-sm border-start border-5 border-{color}"
    )

#====================================
# LAYOUT
#====================================
overview_layout = dbc.Container([
    html.Br(),
    html.H2(
        "Customer Churn Dashboard Overview",
        className="text-center tet-primary fw-bold"
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            create_card(
                "Total Customers",
                f"{total_customers}", "primary"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Churned Customers",
                f"{churned_customers}", "danger"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Churn Rate",
                f"{churn_rate:.2f}%", "warning"
            ),
            md=3
        ),
        dbc.Col(
            create_card(
                "Avg Tenure",
                f"{avg_tenure:.1f} Months", "success"
            ),
            md=3
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=pie_fig)
                ])
            ),
            md=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=tenure_fig)
                ])
            ),
            md=6
        )
    ]),
    html.Br(),
    dbc.Alert(
        [
            html.B("Key Insights: "),
            f"{churn_rate:.1f}% of customer have churned."
            "Most churn occurs among customers with shorter tenure and month-to-month contracts."
        ],
        color="info"
    )
], fluid=True)
