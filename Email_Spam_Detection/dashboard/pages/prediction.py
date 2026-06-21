import joblib
import numpy as np
from scipy.sparse import hstack
from dash import html,dcc
from dash.dependencies import Input,Output,State
import dash_bootstrap_components as dbc
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# =====================================
# LOAD MODEL & VECTORIZER
# =====================================
# model = joblib.load("models/linear_svm.pkl")
model = joblib.load("models/logistic_regression.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
scaler = joblib.load("models/scaler.pkl")
# =====================================
# NLP PREPROCESSING
# =====================================
nltk.download("stopwords")
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# =====================================
# CLEAN TEXT
# =====================================

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"<.*?>"," ",text)
    text = re.sub(r"http\S+|www\S+"," ",text)
    text = re.sub(r"\S+@\S+"," ",text)
    text = re.sub(r"\d+"," ",text)
    text = text.translate(str.maketrans("","",string.punctuation))
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

#======================================
# FEATURE ENGINEERING
#======================================
def transform_email(email_text):
    # -------------------------
    # Manual Features
    # -------------------------
    email_length = len(str(email_text))
    word_count = len(str(email_text).split())
    sentence_count = (
        str(email_text).count(".")
        + str(email_text).count("!")
        + str(email_text).count("?")
    )

    avg_word_length = (
        np.mean(
            [len(word) for word in str(email_text).split()]
        )
        if len(str(email_text).split()) > 0
        else 0
    )

    digit_count = sum(
        c.isdigit()
        for c in str(email_text)
    )

    special_char_count = sum(
        not c.isalnum() and not c.isspace()
        for c in str(email_text)
    )

    manual_features = np.array([
        email_length,
        word_count,
        sentence_count,
        avg_word_length,
        digit_count,
        special_char_count
    ]).reshape(1, -1)
    
    # -------------------------
    # Clean Text
    # -------------------------
    cleaned_email = clean_text(email_text)
    # -------------------------
    # TF-IDF Features
    # -------------------------
    tfidf_features = vectorizer.transform([cleaned_email])
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
            email_vector_scaled = scaler.transform(email_vector)         
            prediction = model.predict(email_vector_scaled)[0]
            probabilities = model.predict_proba(email_vector_scaled)[0]
            spam_risk_score = probabilities[1] * 100
            legitimacy_score = probabilities[0] * 100
            decision_score = model.decision_function(email_vector_scaled)[0]
            # spam_risk_score = (1 /(1 + np.exp(-decision_score))) * 100
            # legitimacy_score = 100 - spam_risk_score

            # =====================
            # Risk Level
            # =====================
            if spam_risk_score >= 80:
                risk_level = "🔴 High Risk Spam"
                risk_color = "danger"
            elif spam_risk_score >= 50:
                risk_level = "🟠 Suspicious Email"
                risk_color = "warning"
            elif spam_risk_score >= 20:
                risk_level = "🟡 Likely Legitimate"
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
                    html.H5(f"Spam Probability: {spam_risk_score:.2f}%"),
                    dbc.Progress(
                        value=spam_risk_score,
                        color="danger",
                        striped=True,
                        animated=True,
                        style={"height":"25px"}
                    ),
                    html.Br(),
                    html.H5(f"Ham Probability: {legitimacy_score:.2f}%"),
                    dbc.Progress(
                        value=legitimacy_score,
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