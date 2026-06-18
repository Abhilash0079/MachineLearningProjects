import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages.overview import overview_layout
from pages.customer_analysis import customer_analyis_layout
from pages.model_performance import model_performance_layout
from pages.explainability import explainability_layout
from pages.prediction import prediction_layout, register_prediction_callback

#====================================
# APP
#====================================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title=("Customer Churn Analytics Dashboard")

# ====================================
# REGISTER PAGE CALLBACKS
# ====================================
register_prediction_callback(app)

#====================================
# LAYOUT
#====================================
app.layout = dbc.Container([
    html.Br(),
    html.Div([
        html.Img(src="assets/telecom_icon.png", height="80px", alt="TelecomImage"),
        html.H1(
            "Customer Churn Analytics Platform", 
            className="fw-bold text-primary text-center"
        )
    ], className="text-center"),
    html.Hr(),
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
                label="Customer Analysis", 
                value="customer_analysis", 
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
    html.Div(id="page-content")
], fluid=True)

#====================================
# CALLBACK
#====================================
@app.callback(
    Output("page-content", "children"),
    Input("tabs", "value")
)

def render_page(tab):
    if tab == "overview":
        return overview_layout
    elif tab == 'customer_analysis':
        return customer_analyis_layout
    elif tab == 'model_performance':
        return model_performance_layout
    elif tab == 'explainability':
        return explainability_layout
    elif tab == "prediction":
        return prediction_layout

#====================================
# RUN
#====================================
if __name__=="__main__":
    app.run(debug=True)