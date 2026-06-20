import pandas as pd
from dash import html,dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# =====================================
# LOAD COEFFICIENTS
# =====================================
coef_df = pd.read_csv("dashboard/data/model_coefficients.csv")

# =====================================
# TOP SPAM WORDS
# =====================================

top_spam = coef_df.sort_values(by="Coefficient",ascending=False).head(15)

# =====================================
# TOP HAM WORDS
# =====================================
top_ham = coef_df.sort_values(by="Coefficient",ascending=True).head(15)

# =====================================
# KPI CARD
# =====================================
def create_card(title,value,color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title,className="kpi-label"),
            html.H3(value,className="kpi-value")
        ]),
        className=f"kpi-card border-start border-5 border-{color}"
    )
# =====================================
# KPI VALUES
# =====================================
top_spam_word = top_spam.iloc[0]["Feature"]
top_ham_word = top_ham.iloc[0]["Feature"]

# =====================================
# SPAM DRIVERS
# =====================================
spam_fig = px.bar(
    top_spam,
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="Top Spam-Indicating Words",
    color="Coefficient",
    text_auto=".2f"
)
spam_fig.update_layout(template="plotly_white",height=650, yaxis=dict(categoryorder="total ascending"))
# =====================================
# HAM CHART
# =====================================
ham_fig = px.bar(
    top_ham,
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="Top Ham-Indicating Words",
    color="Coefficient",
    text_auto=".2f"
)
ham_fig.update_layout(template="plotly_white",height=650)

# =====================================
# PAGE LAYOUT
# =====================================
explainability_layout = dbc.Container([
    html.Br(),
    html.H2("Explainable AI Dashboard",className="page-title"),
    html.Hr(),
    dbc.Alert([
        html.B("Objective: "),
        "Understand which words and features drive spam classification decisions."
    ],
    color="info",className="insight-alert"),
    html.Br(),
    # =================================
    # KPI
    # =================================
    dbc.Row([
        dbc.Col(create_card("Top Spam Driver",top_spam_word,"danger"),md=4),
        dbc.Col(create_card("Top Ham Driver",top_ham_word,"success"),md=4),
        dbc.Col(create_card("Model","Logistic Regression","primary"),md=4)
    ]),
    html.Br(),
    # =================================
    # CHARTS
    # =================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Spam Drivers")),
                dbc.CardBody([dcc.Graph(figure=spam_fig)])
            ],
            className="graph-card"),md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Ham Drivers")),
                dbc.CardBody([dcc.Graph(figure=ham_fig)])
            ],
            className="graph-card"),md=6
        )
    ]),
    html.Br(),
    dbc.Alert([
        html.H5("Key Findings",className="fw-bold"),
        html.Ul([
            html.Li(f"'{top_spam_word}' is the strongest spam-indicating feature."),
            html.Li(f"'{top_ham_word}' is the strongest ham-indicating feature."),
            html.Li("Promotional words significantly increase spam probability."),
            html.Li("Normal conversational language strongly indicates legitimate emails."),
            html.Li("Logistic Regression enables full transparency through feature coefficients.")
        ])
    ],
    color="success",className="insight-alert"),
    html.Br(),
    dbc.Alert([
        html.B("Business Recommendation: "),
        "Messages containing strong promotional and urgency-related keywords should receive higher spam risk scores and trigger enhanced filtering."
    ],
    color="primary",className="insight-alert")
], fluid=True)