import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dashboard.utils.data_loader import load_data

#==========================
# LOAD DATA
#==========================
df = load_data().copy()

# ===================================== 
# CREATE LABEL COLUMN 
# =====================================
df["Label"] = df["Category"].map({ 0: "Ham", 1: "Spam" })

#==========================
# KPIs
#==========================
total_emails = len(df)
spam_emails = (df['Category']==1).sum()
ham_emails = (df['Category']==0).sum()
spam_rate = (spam_emails/total_emails) * 100
avg_word_count = round( df["WordCount"].mean(), 1 )
avg_email_length = round( df["EmailLength"].mean(), 1 )

# ===================================== 
# DEPLOYED MODEL INFO 
# ===================================== 
model_name = "Linear SVM" 
model_accuracy = "98.87%"

#==========================
# KPI CARD
#==========================
def create_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="kpi-label"),
            html.H3(value, className="kpi-value")
        ]),
        className=f"kpi-card border-start border-5 border-{color}"
    )

#==========================
# PIE CHART
#==========================
pie_df = pd.DataFrame({
    "Type":['Ham','Spam'],
    "Count":[ham_emails, spam_emails]
})
pie_fig = px.pie(
    pie_df,
    names="Type",
    values="Count",
    hole=.5,
    title="Spam vs Ham Distribution"
)
pie_fig.update_layout( template="plotly_white" )

# ===================================
# WORD COUNT
# ===================================
word_fig = px.histogram(
    df,
    x="WordCount",
    nbins=40,
    title="Word Count Distribution"
)
word_fig.update_layout( template="plotly_white" )

# ===================================== 
# SPAM VS HAM WORD COUNT 
# ===================================== 
compare_fig = px.box( 
    df, x="Label", 
    y="WordCount", 
    color="Label", 
    title="Spam vs Ham Word Count Comparison" 
) 
compare_fig.update_layout( template="plotly_white" )

# ===================================
# LAYOUT
# ===================================
overview_layout = dbc.Container([
    html.Br(),
    html.H2("Email Spam Detection Dashboard", className="page-title"),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            create_card("Total Emails", total_emails, "primary"),md=4
        ),
        dbc.Col(
            create_card("Spam Emails", spam_emails, "danger"),md=4
        ),
        dbc.Col(
            create_card("Ham Emails", ham_emails, "success"),md=4
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            create_card("Spam Rate", f"{spam_rate:.2f}%", "warning"),md=4
        ),
        dbc.Col(
            create_card("Avg Word Count", avg_word_count, "info"),md=4
        ),
        dbc.Col(
            create_card("Avg Email Length ", avg_email_length, "success"),md=4
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([dcc.Graph(figure=pie_fig)]),
                className="graph-card"
            ), md=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([dcc.Graph(figure=word_fig)]),
                className="graph-card"
            ), md=6
        )
    ]),
    html.Br(),
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(figure=compare_fig)
        ]),
        className="graph-card"
    ),
    html.Br(),
    dbc.Alert([
        html.H5("Key Insights: ", className="fw-bold"),
        html.Ul([ 
            html.Li(f"Dataset contains {total_emails:,} emails."), 
            html.Li(f"{spam_rate:.1f}% of emails are spam."), 
            html.Li("Spam emails generally contain more promotional language and suspicious keywords."), 
            html.Li("Spam messages tend to have higher word counts than legitimate emails."), 
            html.Li("The dataset is reasonably balanced for training machine learning models.") 
        ])
    ], color="info", className="insight-alert"),
    html.Br()
], fluid=True)