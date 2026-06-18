import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

#==============================================
# MODEL PERFORMANCE DATA
#==============================================
performance_df = pd.DataFrame({
    "Model":[
        "Logistic Regression",
        "Random Forest",
        "XGBoost"
    ],
    "Accuracy": [0.799858,0.789922,0.795600],
    "Precision": [0.654362,0.633562,0.641447],
    "Recall": [0.521390,0.494652,0.521390],
    "F1 Score": [0.580357,0.555556,0.575221],
    "ROC AUC": [0.841750,0.825770,0.841436]
})

def create_model_card(title, value, color, icon):
    return dbc.Card(
        dbc.CardBody([
            html.Div(icon, className="kpi-icon"),
            html.H6(title,className="kpi-label"),
            html.H3(value,className=f"text-{color} fw-bold")
        ]),
        className="kpi-card"
    )

#==============================================
# ACCURACY COMPARISON
#==============================================
accuracy_fig = px.bar(
    performance_df,
    x="Model",
    y="Accuracy",
    color="Model",
    text_auto=".3f",
    title="Accuracy Comaprison Across Models"
)

#==============================================
# F1 SCORE COMPARISON
#==============================================
f1_fig = px.bar(
    performance_df,
    x="Model",
    y="F1 Score",
    color="Model",
    text_auto=".3f",
    title="F1 Score Comparison"
)

# =============================================
# ROC AUC COMPARISON
# =============================================
roc_fig = px.bar(
    performance_df,
    x="Model",
    y="ROC AUC",
    color="Model",
    text_auto=".3f",
    title="ROC-AUC Comparison"
)

for fig in [accuracy_fig, f1_fig, roc_fig]:
    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=450,
        font=dict(size=13)
    )
    fig.update_traces(textposition="outside")

# =============================================
# RADAR CHART
# =============================================
radar_df = performance_df.melt(
    id_vars="Model",
    var_name="Metric",
    value_name="Score"
)
radar_fig = px.line_polar(
    radar_df,
    r="Score",
    theta="Metric",
    color="Model",
    line_close=True,
    title="Overall Model Comparison"
)
radar_fig.update_layout(
    template="plotly_white",
    height=650,
    title_x=0.5,
    paper_bgcolor="white"
)

# =============================================
# MODEL INSIGHTS
# =============================================
best_model = performance_df.loc[performance_df['ROC AUC'].idxmax(), "Model"]

# =============================================
# PAGE_LAYOUT
# =============================================
model_performance_layout = dbc.Container([
    # =====================================
    # PAGE BANNER
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Machine Learning Model Evaluation",
                className="text-white fw-bold text-center"
            ),
            html.P(
                "Compare multiple machine learning models and identify the optimal production-ready churn prediction solution.",
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
            html.H4("Project Objective",className="fw-bold"),
            html.P(
                "Evaluate Logistic Regression, Random Forest and XGBoost using multiple performance metrics to identify the best model for customer churn prediction."
            )
        ]),
        className="shadow-sm mb-4"
    ),
    # =====================================
    # KPI CARDS
    # =====================================
    dbc.Row([
        dbc.Col(
            create_model_card(
                "Best Model",
                best_model,
                "success",
                "🏆"
            ),
            md=4
        ),
        dbc.Col(
            create_model_card(
                "Highest ROC-AUC",
                "0.842",
                "primary",
                "📈"
            ),
            md=4
        ),
        dbc.Col(
            create_model_card(
                "Models Evaluated",
                "3",
                "warning",
                "🤖"
            ),
            md=4
        )
    ], className="mb-4"),
    # =====================================
    # PERFORMANCE TABLE
    # =====================================
    dbc.Card([
        dbc.CardHeader(
            html.H4(
                "Model Evaluation Metrics",
                className="mb-0 fw-bold"
            )
        ),
        dbc.CardBody([
            dbc.Table.from_dataframe(
                performance_df.round(3),
                striped=True,
                bordered=True,
                hover=True,
                responsive=True
            )
        ])
    ],
    className="mb-4"),
    # =====================================
    # BAR CHARTS
    # =====================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Accuracy Comparison"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=accuracy_fig,
                        config={"displayModeBar": False}
                    )
                ])
            ]),
            md=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("F1 Score Comparison"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=f1_fig,
                        config={"displayModeBar": False}
                    )
                ])
            ]),
            md=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("ROC-AUC Comparison"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=roc_fig,
                        config={"displayModeBar": False}
                    )
                ])
            ]),
            md=4
        )
    ]),
    html.Br(),
    # =====================================
    # RADAR CHART
    # =====================================
    dbc.Card([
        dbc.CardHeader(
            html.H4(
                "Overall Model Comparison",
                className="mb-0 fw-bold"
            )
        ),
        dbc.CardBody([
            dcc.Graph(
                figure=radar_fig,
                config={"displayModeBar": False}
            )
        ])
    ],
    className="mb-4"),
    # =====================================
    # EXECUTIVE FINDINGS
    # =====================================
    dbc.Alert([
        html.H4("Executive Findings",className="fw-bold"),
        html.Hr(),
        html.Ul([
            html.Li(
                    "Logistic Regression achieved the highest ROC-AUC score (0.842)."
                ),
                html.Li(
                    "XGBoost delivered nearly identical performance."
                ),
                html.Li(
                    "Random Forest showed slightly lower recall and F1 performance."
                ),
                html.Li(
                    "Logistic Regression provides excellent explainability."
                ),
                html.Li(
                    "Model transparency is critical for customer retention strategies."
                )
        ])
    ], color="success",className="shadow-sm mb-4"),
    # =====================================
    # DEPLOYMENT RECOMMENDATION
    # =====================================
    dbc.Card(
        dbc.CardBody([
            html.H4(
                "Production Recommendation",
                className="fw-bold text-primary"
            ),
            html.Hr(),
            html.P(
                "Logistic Regression was selected as the production model because it achieved the highest ROC-AUC score while maintaining strong interpretability. Business stakeholders can clearly understand churn drivers and make data-driven retention decisions."
            )
        ]),
        className="shadow-sm"
    )
], fluid=True)