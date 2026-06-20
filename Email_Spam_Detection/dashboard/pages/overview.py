import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.data_loader import load_data

#==========================
# LOAD DATA
#==========================
df = load_data()

#==========================
# KPIs
#==========================
total_emails = len(df)
spam_emails = (df['Category']==1).sum()
ham_emails = (df['Category']==0).sum()
spam_rate = (spam_emails/total_emails) * 100

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

# ===================================
# WORD COUNT
# ===================================
word_fig = px.histogram(
    df,
    x="WordCount",
    nbins=40,
    title="Word Count Distribution"
)

# ===================================
# CHAR COUNT
# ===================================
char_fig = px.histogram(
    df,
    x="CharCount",
    nbins=40,
    title="Character Count Distribution"
)

# ===================================
# LAYOUT
# ===================================
overview_layout = dbc.Container([
    html.Br(),
    html.H2("Email Spam Detection Dashboard", className="page-title"),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            create_card("Total Emails", total_emails, "primary"),md=3
        ),
        dbc.Col(
            create_card("Spam Emails", spam_emails, "danger"),md=3
        ),
        dbc.Col(
            create_card("Ham Emails", ham_emails, "success"),md=3
        ),
        dbc.Col(
            create_card("Spam Rate", f"{spam_rate:.2f}%", "warning"),md=3
        )
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
            dcc.Graph(figure=char_fig)
        ]),
        className="graph-card"
    ),
    html.Br(),
    dbc.Alert([
        html.B("Key Insights: "),
        f"{spam_rate:.1f}% messages are spam. "
        "Spam messages generally contain more promotional content and suspicious keywords."
    ], color="info", className="insight-alert")
], fluid=True)