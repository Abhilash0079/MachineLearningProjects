import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from pages.overview import overview_layout
from pages.model_performance import model_performance_layout
from pages.explainability import explainability_layout
from pages.prediction import prediction_layout, register_prediction_callback

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ],
    suppress_callback_exceptions=True
)

app.title = "Email Spam Detection | NLP & Machine Learning"

# ====================================
# REGISTER PAGE CALLBACKS
# ====================================
register_prediction_callback(app)

app.layout = dbc.Container([
    html.Div([
        html.H1("📧 Email Spam Detection Platform"),
        html.P("AI-Powered Spam Classification using NLP, TF-IDF and Machine Learning"),
        html.Hr(
            style={
                "backgroundColor":"white",
                "height":"2px",
                "opacity":"0.6"
            }
        ),
        html.H5("Production-Ready Machine Learning Dashboard")
    ],
    className="banner text-center"),
    dcc.Tabs(
        id="tabs",
        value="overview",
        className="custom-tabs",
        children=[
            dcc.Tab(
                label="Overview",
                value="overview",
                className="custom-tab",
                selected_className="custom-tab--selected"
            ),
            dcc.Tab(
                label="Model Performance",
                value="model_performance",
                className="custom-tab",
                selected_className="custom-tab--selected"
            ),
            dcc.Tab(
                label="Explainable AI",
                value="explainability",
                className="custom-tab",
                selected_className="custom-tab--selected"
            ),
            dcc.Tab(
                label="Prediction",
                value="prediction",
                className="custom-tab",
                selected_className="custom-tab--selected"
            )
        ]
    ),
    html.Br(),
    html.Div(id="page-content"),
    html.Br(),
    html.Div([
        html.H5("Email Spam Detection Platform"),
        html.P("Built with Python • NLP • Machine Learning • Dash"),
        html.P("Developed by Abhilash Kumar")
    ],
    className="footer")
], fluid=True)

@app.callback(
    Output("page-content", "children"),
    Input("tabs", "value")
)

def render_page(tab):
    if tab == "overview":
        return overview_layout
    elif tab == 'model_performance':
        return model_performance_layout
    elif tab == "explainability":
        return explainability_layout
    elif tab == "prediction":
        return prediction_layout
    else:
        return "Page Not Found"

if __name__=="__main__":
    app.run(debug=True)