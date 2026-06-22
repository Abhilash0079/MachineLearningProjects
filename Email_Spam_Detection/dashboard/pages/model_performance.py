import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import os

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
    "Accuracy":[0.7269,0.9878,0.9887,0.9852],
    "Precision":[0.4612,0.9851,0.9815,0.9813],
    "Recall":[0.8467,0.9635,0.9708,0.9562],
    "F1 Score":[0.5972,0.9742,0.9761,0.9686],
    "ROC AUC":[0.8329,0.9992,0.9825,0.9980]
})

#=================================
# RELATIVE PATH FOR RENDER
#=================================
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

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
production_model = "Logistic Regression"

production_accuracy = (
    performance_df[
        performance_df["Model"] == "Logistic Regression"
    ]["Accuracy"].iloc[0]
)

production_roc_auc = (
    performance_df[
        performance_df["Model"] == "Logistic Regression"
    ]["ROC AUC"].iloc[0]
)

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
# RECALL CHART
# ======================================
recall_fig = px.bar(
    performance_df,
    x="Model",
    y="Recall",
    color="Model",
    text_auto=".3f",
    title="Recall Comparison"
)

recall_fig.update_layout(
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

roc_path = os.path.join(
    BASE_DIR,
    "data",
    "roc_curve.csv"
)

roc_df = pd.read_csv(roc_path)
#====================
# ROC CURVE
#====================
roc_curve_fig = px.line(
    roc_df,
    x="FPR",
    y="TPR",
    title="ROC Curve"
)

roc_curve_fig.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=1,
    y1=1,
    line=dict(dash="dash")
)

#===============================
# PRECISION-RECALL CURVE
#================================
pr_path = os.path.join(
    BASE_DIR,
    "data",
    "pr_curve.csv"
)
pr_df = pd.read_csv(pr_path)

pr_curve_fig = px.line(
    pr_df,
    x="Recall",
    y="Precision",
    title="Precision-Recall Curve"
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
            create_card("Production Model",production_model,"success"),
            md=4
        ),
        dbc.Col(
            create_card("Accuracy",f"{production_accuracy:.2%}","primary"),
            md=4
        ),
        dbc.Col(
            create_card("ROC-AUC",f"{production_roc_auc:.2%}","warning"),
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
            className="graph-card"),md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=recall_fig)
                ])
            ],
            className="graph-card"),md=6
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=f1_fig)
                ])
            ],
            className="graph-card"),md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=roc_fig)
                ])
            ],
            className="graph-card"),md=6
        ),
    ]),
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
    className="graph-card"
    ),
    html.Br(),
    html.H4("Advanced Evaluation Curves",className="section-title mb-3"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=roc_curve_fig)
                ])
            ]),
            md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=pr_curve_fig)
                ])
            ]),
            md=6
        )
    ]),
    dbc.Card([
        dbc.CardBody([
            html.Img(src="assets/confusion_matrix.png",
                style={
                "width": "100%",
                "borderRadius": "10px"
                }
            )
        ])
    ],
    className="graph-card"),
    html.Br(),
    html.H4("Business Insights & Recommendations",className="section-title mb-3"),
    dbc.Alert([
        html.H5("Key Findings:",className="fw-bold"),
        html.Ul([
            html.Li("Linear SVM delivered the highest F1 Score and Recall."),
            html.Li("Logistic Regression achieved highest Precision and ROC-AUC."),
            html.Li("Logistic Regression selected as the production model.")
        ])
    ],
    color="success",
    className="insight-alert")
], fluid=True)