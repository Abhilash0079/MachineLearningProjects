import joblib
import numpy as np
from scipy.sparse import hstack
from dash import html,dcc
from dash.dependencies import Input,Output,State
import dash_bootstrap_components as dbc

# =====================================
# LOAD MODEL & VECTORIZER
# =====================================
model = joblib.load("models/linear_svm.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

#======================================
# FEATURE ENGINEERING
#======================================
def transform_email(email_text):
    # -------------------------
    # Manual Features
    # -------------------------
    char_count = len(str(email_text))
    word_count = len(str(email_text).split())
    sentence_count = (
        str(email_text).count(".")
        + str(email_text).count("!")
        + str(email_text).count("?")
    )
    avg_word_length = (np.mean([len(word) for word in str(email_text).split()])
        if len(str(email_text).split()) > 0
        else 0
    )

    manual_features = np.array([
        char_count,
        word_count,
        sentence_count,
        avg_word_length
    ]).reshape(1, -1)

    # -------------------------
    # TF-IDF Features
    # -------------------------
    tfidf_features = vectorizer.transform([email_text])
    # -------------------------
    # Combine Features
    # -------------------------
    final_features = hstack([manual_features,tfidf_features])
    return final_features.toarray()
# =====================================
# PAGE LAYOUT
# =====================================
prediction_layout = dbc.Container([
    html.Br(),
    html.H1(
        "Email Spam Prediction",
        className="page-title text-center"
    ),
    html.P(
        "Detect suspicious emails using Machine Learning and NLP",
        className="text-center text-light fs-5"
    ),
    html.Br(),
    dbc.Card([
        dbc.CardBody([
            html.H3("Email Content",className="fw-bold mb-3"),
            dcc.Textarea(
                id="email-input",
                placeholder="Paste your email content here...",
                style={"width":"100%","height":"300px"}
            ),
            html.Br(),
            html.Br(),
            dbc.Button(
                "Predict",
                id="predict-btn",
                color="primary",
                size="lg",
                className="custom-btn"
            )
        ])
    ], className="graph-card"),
    html.Br(),
    html.Div(id="prediction-output")
], fluid=True)
# =====================================
# CALLBACK
# =====================================
def register_prediction_callback(app):
    @app.callback(
        Output("prediction-output","children"),
        Input("predict-btn","n_clicks"),
        State("email-input","value")
    )
    def predict_email(n_clicks,email_text):
        if not n_clicks:
            return ""
        if not email_text:
            return dbc.Alert("Please enter email content.",color="warning")

        # ============================
        # VECTORIZE
        # ============================
        try:
            email_vector = transform_email(email_text)            
            prediction = model.predict(email_vector)[0]
            decision_score = model.decision_function(email_vector)[0]
            spam_probability = (1 /(1 + np.exp(-decision_score))) * 100
            ham_probability = 100 - spam_probability

            # =====================
            # Risk Level
            # =====================
            if spam_probability >= 80:
                risk_level = "🔴 High Risk Spam"
                risk_color = "danger"
            elif spam_probability >= 50:
                risk_level = "🟠 Suspicious Email"
                risk_color = "warning"
            elif spam_probability >= 20:
                risk_level = "🟡 Promotional Email"
                risk_color = "info"
            else:
                risk_level = "🟢 Safe Email"
                risk_color = "success"

            # =====================
            # Email Statistics
            # =====================
            char_count = len(email_text)
            word_count = len(email_text.split())
            sentence_count = (
                email_text.count(".")
                + email_text.count("!")
                + email_text.count("?")
            )
            avg_word_length = (
                np.mean(
                    [len(word)
                     for word in email_text.split()]
                )
                if len(email_text.split()) > 0
                else 0
            )
            return dbc.Card([ 
                dbc.CardHeader(
                    html.H2("Prediction Results",className="text-center text-white mb-0"),
                    className="bg-primary"
                ),
                dbc.CardBody([
                    html.H1(
                        "🚨 SPAM EMAIL"
                        if prediction == 1
                        else "✅ HAM EMAIL",
                        className=(
                            "text-danger text-center fw-bold"
                            if prediction == 1
                            else "text-success text-center fw-bold"
                        )
                    ),
                    html.H4(risk_level,className=f"text-{risk_color} text-center"),
                    html.Hr(),
                    html.H5(f"Spam Probability: {spam_probability:.2f}%"),
                    dbc.Progress(
                        value=spam_probability,
                        color="danger",
                        striped=True,
                        animated=True,
                        style={"height":"25px"}
                    ),
                    html.Br(),
                    html.H5(f"Ham Probability: {ham_probability:.2f}%"),
                    dbc.Progress(
                        value=ham_probability,
                        color="success",
                        striped=True,
                        animated=True,
                        style={"height":"25px"}
                    ),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Characters"),
                                    html.H3(char_count,className="text-primary")
                                ])
                            ], className="stat-card"),md=3
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Words"),
                                    html.H3(word_count,className="text-success")
                                ])
                            ], className="stat-card"),md=3
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Sentences"),
                                    html.H3(sentence_count,className="text-warning")
                                ])
                            ], className="stat-card"),md=3
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("Avg Word Length"),
                                    html.H3(f"{avg_word_length:.1f}",className="text-info")
                                ])
                            ], className="stat-card"),md=3
                        )
                    ])
                ]) 
            ], className="prediction-card shadow-lg")
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger")