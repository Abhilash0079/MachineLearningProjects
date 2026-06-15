import pandas as pd
import plotly.express as px
from dash import html, dcc
# =====================================
# LOAD TEST PREDICTIONS
# =====================================

pred_df = pd.read_csv("data/predictions/test_predictions.csv")

# =====================================
# MODEL METRICS
# =====================================

RF_R2 = 0.9786
RF_RMSE = 27495.37

XGB_R2 = 0.9798
XGB_RMSE = 26749.00

# =====================================
# FEATURE IMPORTANCE
# =====================================

importance_df = pd.DataFrame({
    "Feature": [
        "lag_7",
        "month",
        "cases_7d_avg",
        "lag_14",
        "mortality_rate",
        "vaccination_rate",
        "cases_14d_avg",
        "lag_1",
        "weekday"
    ],
    "Importance": [
        0.747064,
        0.130515,
        0.122148,
        0.000170,
        0.000052,
        0.000032,
        0.000020,
        0.000000,
        0.000000
    ]
})

# =====================================
# ACTUAL VS PREDICTED
# =====================================

actual_pred_fig = px.line(pred_df.head(200),y=["actual_cases","predicted_cases"],title="Actual vs Predicted Cases")

# =====================================
# FEATURE IMPORTANCE
# =====================================

importance_fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance (XGBoost)"
)

# =====================================
# LAYOUT
# =====================================

performance_layout = html.Div([
    html.H1(
        "Model Performance Dashboard", className="text-info"
    ),
    html.Br(),
    # KPI Cards
    html.Div([
        html.Div([
            html.H3("Random Forest"),
            html.H2(
                f"R² = {RF_R2}"
            ),
            html.P(
                f"RMSE = {RF_RMSE:,.0f}"
            )
        ], className="card"),
        html.Div([
            html.H3("XGBoost"),
            html.H2(
                f"R² = {XGB_R2}"
            ),
            html.P(
                f"RMSE = {XGB_RMSE:,.0f}"
            )
        ], className="card")
    ], style={
        "display": "flex",
        "gap": "20px"
    }),
    html.Br(),
    dcc.Graph(figure=actual_pred_fig),
    html.Br(),
    dcc.Graph(figure=importance_fig)
], className="text-center mb-4 fw-bold text-secondary")