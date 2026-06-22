import pandas as pd
from dash import html,dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import os

# =====================================
# LOAD COEFFICIENTS
# =====================================
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

coef_path = os.path.join(
    BASE_DIR,
    "data",
    "lr_model_coefficients.csv"
)
coef_df = pd.read_csv(coef_path)

# =====================================
# TOP SPAM WORDS
# =====================================

top_spam = coef_df.sort_values(by="Coefficient",ascending=False).head(15)

# =====================================
# TOP HAM WORDS
# =====================================
top_ham = coef_df.sort_values(by="Coefficient",ascending=True).head(15)

# =====================================
# KPI CARD
# =====================================
def create_card(title,value,color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title,className="kpi-label"),
            html.H3(value,className="kpi-value")
        ]),
        className=f"kpi-card border-start border-5 border-{color}"
    )
# =====================================
# KPI VALUES
# =====================================
top_spam_word = top_spam.iloc[0]["Feature"]
top_ham_word = top_ham.iloc[0]["Feature"]
total_features = len(coef_df)
# =====================================
# SPAM DRIVERS
# =====================================
spam_fig = px.bar(
    top_spam,
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="Top Spam-Indicating Words",
    color="Coefficient",
    text_auto=".2f"
)
spam_fig.update_layout(template="plotly_white",height=650, yaxis=dict(categoryorder="total ascending"))
# =====================================
# HAM CHART
# =====================================
ham_fig = px.bar(
    top_ham,
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="Top Ham-Indicating Words",
    color="Coefficient",
    text_auto=".2f"
)
ham_fig.update_layout(template="plotly_white",height=650)

# ===================================== 
# MOST INFLUENTIAL FEATURES 
# ===================================== 
overall_features = pd.concat([top_spam.head(10), top_ham.head(10)]) 
overall_fig = px.bar(
    overall_features, 
    x="Coefficient", 
    y="Feature", 
    orientation="h", 
    color="Coefficient", 
    title="Most Influential Features", 
    text_auto=".2f" 
) 
overall_fig.update_layout(template="plotly_white", height=700)

# =====================================
# PAGE LAYOUT
# =====================================
explainability_layout = dbc.Container([
    html.Br(),
    html.H2("Explainable AI Dashboard",className="page-title"),
    html.Hr(),
    dbc.Alert([
        html.B("Objective: "),
        "Understand which words and features drive spam classification decisions."
    ],
    color="info",className="insight-alert"),
    html.Br(),
    # =================================
    # KPI
    # =================================
    dbc.Row([
        dbc.Col(create_card("Top Spam Driver",top_spam_word,"danger"),md=4),
        dbc.Col(create_card("Top Ham Driver",top_ham_word,"success"),md=4),
        dbc.Col(create_card("Feature Analyzed",f"{total_features}","primary"),md=4)
    ]),
    html.Br(),
    # =================================
    # CHARTS
    # =================================
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Spam Drivers")),
                dbc.CardBody([dcc.Graph(figure=spam_fig)])
            ],
            className="graph-card"),md=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Ham Drivers")),
                dbc.CardBody([dcc.Graph(figure=ham_fig)])
            ],
            className="graph-card"),md=6
        )
    ]),
    html.Br(),
    dbc.Card([ 
        dbc.CardHeader( 
            html.H4("Most Influential Features") 
        ), 
        dbc.CardBody([ 
            dcc.Graph(figure=overall_fig) 
        ]) 
    ], className="graph-card"
    ),
    html.Br(),
    dbc.Alert([
        html.H5("Key Findings",className="fw-bold"),
        html.Ul([ 
            html.Li( f"'{top_spam_word}' is the strongest spam-indicating feature." ), 
            html.Li( f"'{top_ham_word}' is the strongest ham-indicating feature." ), 
            html.Li( f"{total_features:,} features were analyzed during model interpretation." ), 
            html.Li( "Promotional and urgency-related words strongly increase spam probability." ), 
            html.Li( "Conversational and workplace-related language strongly indicates legitimate emails." ), 
            html.Li( "Feature coefficients provide transparency into model decision-making." ) 
        ])
    ],
    color="success",className="insight-alert"),
    html.Br(),
    dbc.Alert([ 
        html.B( "Business Recommendation: " ), 
        "Messages containing strong promotional, urgency, reward, discount, or financial keywords should receive elevated spam risk scores and be prioritized for automated filtering." 
    ],
    color="primary",className="insight-alert")
], fluid=True)