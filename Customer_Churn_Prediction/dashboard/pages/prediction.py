import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from utils.prediction_helper import predict_customer

# =====================================================
# PAGE LAYOUT
# =====================================================
prediction_layout = dbc.Container([
    html.Br(),
    html.H2(
        "Customer Churn Prediction Tool",
        className="text-center fw-bold text-primary"
    ),
    html.Hr(),
    dbc.Alert(
        [
            html.B("Objective: "),
            "Predict whether a customer is likely to churn based on customer profile and subscription details."
        ],color="info"
    ),
    dbc.Row([
        # =================================================
        # INPUT FORM
        # =================================================
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Customer Information")),
                dbc.CardBody([
                    html.Label("Gender"),
                    dcc.Dropdown(
                        id="gender",
                        options=[
                            {"label": "Male", "value": "Male"},
                            {"label": "Female", "value": "Female"}
                        ],value="Male"
                    ),
                    html.Br(),
                    html.Label("Senior Citizen"),
                    dcc.Dropdown(
                        id="senior",
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0}
                        ],value=0
                    ),
                    html.Br(),
                    html.Label("Partner"),
                    dcc.Dropdown(
                        id="partner",
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0}
                        ],value=0
                    ),
                    html.Br(),
                    html.Label("Dependents"),
                    dcc.Dropdown(
                        id="dependents",
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0}
                        ],value=0
                    ),
                    html.Br(),
                    html.Label("Tenure (Months)"),
                    dcc.Input(
                        id="tenure",
                        type="number",
                        value=12,
                        className="form-control"
                    ),
                    html.Br(),
                    html.Label("Monthly Charges"),
                    dcc.Input(
                        id="monthlycharges",
                        type="number",
                        value=70,
                        className="form-control"
                    ),
                    html.Br(),
                    html.Label("Total Charges"),
                    dcc.Input(
                        id="totalcharges",
                        type="number",
                        value=840,
                        className="form-control"
                    ),
                ])
            ])
        ], width=4),
        # =================================================
        # SERVICE DETAILS
        # =================================================
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Subscription Details")),
                dbc.CardBody([
                    html.Label("Phone Service"),
                    dcc.Dropdown(
                        id="phoneservice",
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0}
                        ],value=1
                    ),
                    html.Br(),
                    html.Label("Multiple Lines"),
                    dcc.Dropdown(
                        id="multiplelines",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No phone service", "value": "No phone service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Internet Service"),
                    dcc.Dropdown(
                        id="internetservice",
                        options=[
                            {"label": "DSL", "value": "DSL"},
                            {"label": "Fiber optic", "value": "Fiber optic"},
                            {"label": "No", "value": "No"}
                        ],value="Fiber optic"
                    ),
                    html.Br(),
                    html.Label("Online Security"),
                    dcc.Dropdown(
                        id="onlinesecurity",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Online Backup"),
                    dcc.Dropdown(
                        id="onlinebackup",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Device Protection"),
                    dcc.Dropdown(
                        id="deviceprotection",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Tech Support"),
                    dcc.Dropdown(
                        id="techsupport",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    )
                ])
            ])
        ], width=4),
        # =================================================
        # BILLING DETAILS
        # =================================================
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Billing Details")),
                dbc.CardBody([
                    html.Label("Streaming TV"),
                    dcc.Dropdown(
                        id="streamingtv",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Streaming Movies"),
                    dcc.Dropdown(
                        id="streamingmovies",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            {"label": "No internet service", "value": "No internet service"}
                        ],value="No"
                    ),
                    html.Br(),
                    html.Label("Paperless Billing"),
                    dcc.Dropdown(
                        id="paperless",
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0}
                        ],value=1
                    ),
                    html.Br(),
                    html.Label("Contract"),
                    dcc.Dropdown(
                        id="contract",
                        options=[
                            {"label": "Month-to-month", "value": "Month-to-month"},
                            {"label": "One year", "value": "One year"},
                            {"label": "Two year", "value": "Two year"}
                        ],value="Month-to-month"
                    ),
                    html.Br(),
                    html.Label("Payment Method"),
                    dcc.Dropdown(
                        id="paymentmethod",
                        options=[
                            {"label": "Electronic check", "value": "Electronic check"},
                            {"label": "Credit card (automatic)", "value": "Credit card (automatic)"},
                            {"label": "Bank transfer (automatic)", "value": "Bank transfer (automatic)"},
                            {"label": "Mailed check", "value": "Mailed check"}
                        ],value="Electronic check"
                    ),
                    html.Br(),
                    dbc.Button(
                        "Predict Churn",
                        id="predict-button",
                        color="primary",
                        size="lg",
                        className="w-100"
                    )
                ])
            ])
        ], width=4)
    ]),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H4("Prediction Result")),
        dbc.CardBody(html.Div(id="prediction-output"))
    ])
], fluid=True)

# =====================================================
# CALLBACK FUNCTION
# =====================================================

def register_prediction_callback(app):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-button", "n_clicks"),

        State("gender", "value"),
        State("senior", "value"),
        State("partner", "value"),
        State("dependents", "value"),
        State("tenure", "value"),
        State("phoneservice", "value"),
        State("paperless", "value"),
        State("monthlycharges", "value"),
        State("totalcharges", "value"),
        State("multiplelines", "value"),
        State("internetservice", "value"),
        State("onlinesecurity", "value"),
        State("onlinebackup", "value"),
        State("deviceprotection", "value"),
        State("techsupport", "value"),
        State("streamingtv", "value"),
        State("streamingmovies", "value"),
        State("contract", "value"),
        State("paymentmethod", "value")
    )

    def predict(
        n_clicks,
        gender,
        senior,
        partner,
        dependents,
        tenure,
        phoneservice,
        paperless,
        monthlycharges,
        totalcharges,
        multiplelines,
        internetservice,
        onlinesecurity,
        onlinebackup,
        deviceprotection,
        techsupport,
        streamingtv,
        streamingmovies,
        contract,
        paymentmethod
    ):
        if not n_clicks:
            return "Enter customer details and click Predict."
        data = {
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phoneservice,
            "PaperlessBilling": paperless,
            "MonthlyCharges": monthlycharges,
            "TotalCharges": totalcharges,

            "gender": gender,
            "MultipleLines": multiplelines,
            "InternetService": internetservice,
            "OnlineSecurity": onlinesecurity,
            "OnlineBackup": onlinebackup,
            "DeviceProtection": deviceprotection,
            "TechSupport": techsupport,
            "StreamingTV": streamingtv,
            "StreamingMovies": streamingmovies,
            "Contract": contract,
            "PaymentMethod": paymentmethod
        }
        prediction, probability = predict_customer(data)
        probability_pct = probability * 100
        if probability_pct < 30:
            risk = "LOW"
            color = "success"
        elif probability_pct < 70:
            risk = "MEDIUM"
            color = "warning"
        else:
            risk = "HIGH"
            color = "danger"
        recommendation = {
            "LOW":
                "Customer appears stable. Continue engagement programs.",
            "MEDIUM":
                "Offer personalized promotions and monitor activity.",
            "HIGH":
                "Immediate retention campaign recommended. Consider contract upgrade incentives."
        }
        return dbc.Alert(
            [
                html.H3(f"Churn Probability: {probability_pct:.2f}%"),
                html.H4(f"Risk Level: {risk}"),
                html.Hr(),
                html.P(recommendation[risk])
            ],color=color
        )