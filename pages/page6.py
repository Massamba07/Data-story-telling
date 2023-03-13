from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import styles
import pandas as pd
import numpy as np
from pages import gen

df = pd.read_csv("./datasets/FAOSTAT_prix_prod.csv", index_col=0)
an = np.sort(df.Année.unique())
continents = df.Zone.unique()
products = df.Produit.unique()

# SIMPLE TABLE
table = html.Div(
    dash_table.DataTable(
        id="table_p3",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        filter_options={"placeholder_text": "Filtrer"},
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
        style_header={
            'backgroundColor': 'rgba(0, 0, 0, 0)'
        },
        style_filter={
            'backgroundColor': 'rgba(0, 0, 0, 0)'
        },
        style_data={
            'backgroundColor': 'rgba(0, 0, 0, 0)'
        }
    ),
    className="dbc-row-selectable"
)

# CHANGER L'AFFICHAGE DES TABS
tab7 = dbc.Tab([dcc.Graph(id="line-okk")], label="Bar Chart")
tab_9 = dbc.Tab([table], label="Table", className="p-4")
tabs10 = dbc.Card(dbc.Tabs([tab7, tab_9]))

# ===========================================================================================================================================

layout6 = dbc.Row(
    [
        dbc.Col(
            [
                tabs10
            ],
            style={"height": "70%", "width": "40%", "display": "inline-block"}
        )
    ],
    style=styles.CONTENT_STYLE
)


@callback(
    Output("line-okk", "figure"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def upgrade_it(theme):
    df = pd.read_csv("./datasets/FAOSTAT_prix_prod.csv", index_col=0)
    df = df.copy()
    df = pd.DataFrame(df.groupby("Produit")["norm_price"].mean().sort_values(ascending=False).head(8))
    fig4 = px.bar(df, x=df.index, y="norm_price", template=template_from_url(theme))
    fig4.update_layout(
        xaxis_title="Produits",
        yaxis_title="Prix"
    )

    return fig4
