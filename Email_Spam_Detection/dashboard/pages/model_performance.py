import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# ======================================
# MODEL RESULTS
# ======================================
performance_df = pd.DataFrame({
    "Model":[
        "Naive Bayes",
        "Logistic Regression",
        "Linear SVM",
        "Random Forest"
    ],
    "Accuracy":[0.9704,0.9686,0.9865,0.9803],
    "Precision":[1.0000,0.9600,0.9927,1.0000],
    "Recall":[0.7800,0.8000,0.9067,0.8533],
    "F1 Score":[0.8764,0.8727,0.9477,0.9209],
    "ROC AUC":[0.9838,0.9914,0.9528,0.9890]
})

# ======================================
# KPI CARD
# ======================================
def create_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="kpi-label"),
            html.H3(value,className="kpi-value")
        ]),
        className=f"kpi-card border-start border-5 border-{color}"
    )

# ======================================
# BEST MODEL
# ======================================
best_model = "Linear SVM"
best_accuracy = performance_df["Accuracy"].max()
best_f1 = performance_df["F1 Score"].max()

# ======================================
# ACCURACY CHART
# ======================================
accuracy_fig = px.bar(
    performance_df,
    x="Model",
    y="Accuracy",
    color="Model",
    text_auto=".3f",
    title="Accuracy Comparison"
)
accuracy_fig.update_layout(
    template="plotly_white",
    showlegend=False
)

# ======================================
# F1 CHART
# ======================================
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
    showlegend=False
)

# ======================================
# ROC AUC
# ======================================
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
    showlegend=False
)

# ======================================
# RADAR CHART
# ======================================
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
    # title="Overall Model Comparison"
)

radar_fig.update_layout(
    height=700
)

# ======================================
# PAGE LAYOUT
# ======================================
model_performance_layout = dbc.Container([
    html.Br(),
    html.H2("Model Performance Dashboard",className="page-title"),
    html.Hr(),
    dbc.Alert([
        html.B("Objective: "),
        "Compare multiple machine learning algorithms and select the most effective spam detection model."
    ],
    color="info",className="insight-alert"),
    html.Br(),
    # ==================================
    # KPI CARDS
    # ==================================
    html.H4("Performance Summary",className="section-title mb-3"),
    dbc.Row([
        dbc.Col(
            create_card("Best Model",best_model,"success"),
            md=4
        ),
        dbc.Col(
            create_card("Best Accuracy",f"{best_accuracy:.2%}","primary"),
            md=4
        ),
        dbc.Col(
            create_card("Best F1 Score",f"{best_f1:.2%}","warning"),
            md=4
        )
    ]),
    html.Br(),
    # ==================================
    # PERFORMANCE TABLE
    # ==================================
    html.H4("Model Evaluation Metrics",className="section-title mb-3"),
    dbc.Card([
        # dbc.CardHeader(
        #     html.H4("Model Evaluation Metrics")
        # ),
        dbc.CardBody([
            dbc.Table.from_dataframe(
                performance_df.round(4),
                striped=True,
                bordered=True,
                hover=True,
                responsive=True
            )
        ])
    ],
    className="table-card"),
    html.Br(),

    # ==================================
    # CHARTS
    # ==================================
    html.H4("Model Performance Comparison",className="section-title mb-3"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=accuracy_fig)
                ])
            ],
            className="graph-card"),md=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=f1_fig)
                ])
            ],
            className="graph-card"),md=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=roc_fig)
                ])
            ],
            className="graph-card"),md=4
        )
    ]),
    html.Br(),
    # ==================================
    # RADAR
    # ==================================
    html.H4("Comprehensive Model Analysis",className="section-title mb-3"),
    dbc.Card([
        # dbc.CardHeader(
        #     html.H4("Overall Model Comparison")
        # ),
        dbc.CardBody([
            dcc.Graph(figure=radar_fig)
        ])
    ],
    className="graph-card"),
    html.Br(),
    html.H4("Business Insights & Recommendations",className="section-title mb-3"),
    dbc.Alert([
        html.H5("Key Findings:",className="fw-bold"),
        html.Ul([
            html.Li("Linear SVM achieved the highest overall performance."),
            html.Li("Linear SVM delivered the highest F1 Score and Recall."),
            html.Li("Random Forest achieved perfect Precision."),
            html.Li("Logistic Regression achieved the highest ROC-AUC."),
            html.Li("Linear SVM selected as the production model.")
        ])
    ],
    color="success",
    className="insight-alert")
], fluid=True)