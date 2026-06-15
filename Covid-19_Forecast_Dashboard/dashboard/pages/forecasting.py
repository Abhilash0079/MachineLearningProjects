import pandas as pd
import plotly.express as px
from dash import html, dcc

#==================================
# LOAD FORECAST DATA
#==================================
forecast_df = pd.read_csv("data/forecast/xgboost_forecast.csv")
forecast_df['date'] = pd.to_datetime(forecast_df['date'])

#==================================
# FORECAST SUMMARY
#==================================
total_forecast_cases = int(forecast_df['predicted_cases'].sum())
peak_forecast_cases = int(forecast_df['predicted_cases'].max())

peak_date = (forecast_df.loc[forecast_df['predicted_cases'].idxmax(),'date']).strftime("%d %b %Y")

#=================================
# FORECAST CHART
#=================================
forecast_fig = px.line(
    forecast_df,
    x='date',
    y='predicted_cases',
    markers=True,
    title="30-Day COVID Cases Forecast"
)
forecast_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Predicted Cases"
)

#===============================
# TABLE
#==============================
forecast_table = forecast_df.head(30)

#==============================
# LAYOUT
#==============================
forecast_layout = html.Div([
    html.H1("COVID-19 Forecasting Dashboard", className="text-center mb-4 fw-bold text-warning"),
    html.P("Experimental forecast generated using XGBoost and lag-based features.", className="text-center mb-4 fw-bold text-info"),
    html.Br(), 

    # KPI Cards
    html.Div([
        html.Div([
            html.H4("Total Forecast Cases"),
            html.H2(f"{total_forecast_cases:,}")
        ], className="card"),
        html.Div([
            html.H4("Peak Forecast Cases"),
            html.H2(f"{peak_forecast_cases:,}")
        ],className='card'),
        html.Div([
            html.H4("Peak Forecast Date"),
            html.H2(peak_date)
        ], className="card")
    ], style={"display":"flex", "gap":"20px"}),
    html.Br(),

    dcc.Graph(figure=forecast_fig),
    html.Br(),
    html.H3("Forecast Data"),
    dcc.Graph(figure=px.bar(
        forecast_df,
        x='date',
        y='predicted_cases',
        title="Daily Forecast Cases"
    ))
])