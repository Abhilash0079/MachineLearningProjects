import pandas as pd
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from pages.overview import overview_layout
from pages.trends import trends_layout
from pages.vaccination import vaccination_layout
from pages.forecasting import forecast_layout
from pages.model_performance import performance_layout

# =====================================
# APP
# =====================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.title="India COVID-19 Forecast Dashboard"
# =====================================
# LAYOUT
# =====================================
app.layout = dbc.Container([
    html.Div([
        html.Img(src="/assets/covid_icon.png",height="80px"),
        html.H1("India COVID-19 Forecast Dashboard",className="text-center my-4 fw-bold text-primary"),
        html.P("Machine Learning Powered COVID Intelligence Platform",className="dashboard-subtitle"),
        html.Hr(),
    ], className="header-container"),
    
    dcc.Tabs(
        id='tabs',
        value='overview',
        children=[
            dcc.Tab(label='📊 Overview', value='overview'),
            dcc.Tab(label='📈 Trends', value='trends'),
            dcc.Tab(label='💉 Vaccination', value='vaccination'),
            dcc.Tab(label='🤖 Model Performance', value='performance'),
            dcc.Tab(label='🔮 Forecasting', value='forecasting')
        ]
    ),
    html.Br(),
    html.Div(id='page-content'),
    html.Hr(),
    #Footer
    html.Div("Built with Python • Dash • Plotly • Scikit-Learn • XGBoost",className="footer")
], fluid=True)

#============================
# CALLBACK
#============================
@app.callback(
    Output('page-content', 'children'),
    Input('tabs', 'value')
)

def render_page(tab):
    if tab == 'overview':
        return overview_layout
    elif tab == 'trends':
        return trends_layout
    elif tab == 'vaccination':
        return vaccination_layout
    elif tab == 'performance':
        return performance_layout
    elif tab == 'forecasting':
        return forecast_layout

# =====================================
# TRENDS CALLBACK
# =====================================

@app.callback(
    Output("cases-trend", "figure"),
    Output("ma-trend", "figure"),
    Output("deaths-trend", "figure"),

    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_trends(start_date, end_date):

    df = pd.read_csv("data/processed/india_ml_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])

    filtered_df = df[(df["date"] >= start_date)&(df["date"] <= end_date)]

    # Cases Trend
    cases_fig = px.line(
        filtered_df,
        x="date",
        y="cases_7d_avg",
        title="7-Day Average COVID Cases"
    )
    cases_fig.update_layout(
        template="plotly_white"
    )

    # Moving Average
    ma_fig = px.line(
        filtered_df,
        x="date",
        y=["cases_7d_avg","cases_14d_avg"],
        title="7-Day vs 14-Day Average"
    )
    ma_fig.update_layout(
        template="plotly_white"
    )

    # Death Trend
    death_fig = px.line(
        filtered_df,
        x="date",
        y="new_deaths",
        title="Daily COVID Deaths"
    )
    death_fig.update_layout(
        template="plotly_white"
    )

    return (cases_fig, ma_fig, death_fig)

#=====================
# RUN
#=====================
if __name__=="__main__":
    app.run(debug=True)