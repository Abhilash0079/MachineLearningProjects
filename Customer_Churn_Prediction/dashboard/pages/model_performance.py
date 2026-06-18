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
accuracy_fig.update_layout(
    template="plotly_white",
    height=450,
    showlegend=False
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
f1_fig.update_layout(
    template="plotly_white",
    height=450,
    showlegend=False
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
roc_fig.update_layout(
    template="plotly_white",
    height=450,
    showlegend=False
)

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
radar_fig.update_layout(height=700)

# =============================================
# MODEL INSIGHTS
# =============================================
best_model = performance_df.loc[performance_df['ROC AUC'].idxmax(), "Model"]

# =============================================
# PAGE_LAYOUT
# =============================================
model_performance_layout = dbc.Container([
    html.Br(),
    html.H2(
        "Machine Learning Model Performance",
        className="text-center fw-bold text-primary"
    ),
    html.Hr(),
    dbc.Alert([
        html.B("Project Overview: "),
        "Evaluate multiple machine learning algorithms and select the most effective model for customer churn prediction."
    ], color="info"),
    #===============================
    # PERFORMANCE TABLE
    #===============================
    dbc.Card([
        dbc.CardHeader(
            html.H4(
                "Model Evaluation Matrics", className="mb-0"
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
    ]),
    html.Br(),
    #=============================
    # KPI CARDS
    #=============================
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6("Best Model"),
                    html.H3(best_model, className="text-success")
                ]),
                className="shadow-sm border-success"
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6("Highest ROC-AUC"),
                    html.H3("0.842", className="text-primary")
                ]),
                className="shadow-sm border-primary"
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6("Model Compared"),
                    html.H3("3", className="text-warning")
                ]),
                className="shadow-sm border-warning"
            ),
            width=4
        )
    ]),
    html.Br(),
    #======================
    # BAR CHARTS
    #======================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=accuracy_fig)
                ])
            ]),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=f1_fig)
                ])
            ]),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=roc_fig)
                ])
            ]),
            width=4
        )
    ]),
    html.Br(),
    #=========================
    # RADAR CHART
    #=======================
    dbc.Card([
        dbc.CardHeader(
            html.H4("Model Comparison Radar Chart", className="mb-0")
        ),
        dbc.CardBody([
            dcc.Graph(figure=radar_fig)
        ])
    ]),
    html.Br(),
    #=========================
    # INSIGHTS
    #========================
    dbc.Alert([
        html.H5("Key Findings: ", className="fw-bold"),
        html.Ul([
            html.Li(
                "Logistic Regression achieved the highest ROC-AUC score."
            ),
            html.Li(
                "XGBoost delivered performance very close to Logistic Regression."
            ),
            html.Li(
                "Random Forest showed slightly lower recall and F1 score."
            ),
            html.Li(
                "Logistic Regression provides superior interpretability for business stakeholders."
            ),
            html.Li("Selected as the final production model.")
        ])
    ], color="success"),
    html.Br(),
    dbc.Alert([
        html.B("Business Recommendation: "),
        "Deploy Logistic Regression as the production churn prediction model because it balances strong predictive performance with transparency and explainability."
    ], color="primary")
], fluid=True)