import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from pages.overview import overview_layout
# from pages.world_map import map_layout
# from pages.country_analysis import country_layout
# from pages.forecasting import forecast_layout
# from pages.model_performance import performance_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title="COVID-19 Forecast Dashboard"
app.layout = dbc.Container([
    html.H1(
        "COVID-19 Forecast Dashboard",
        className="text-center my-4 fw-bold text-primary"
    ),
    overview_layout
], fluid=True)


if __name__=="__main__":
    app.run(debug=True)