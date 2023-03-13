from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import styles
import pandas as pd
import numpy as np
from pages import gen

df = pd.read_csv("./datasets/wfp_foodprices_norm_clean.csv", index_col=0)
an = np.sort(df.mp_year.unique())
continents = df.Pays.unique()
products = df.Produit.unique()

# SIMPLE TABLE
table = html.Div(
    dash_table.DataTable(
        id="table_p2",
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
tab7 = dbc.Tab([dcc.Graph(id="line-chart_p2")], label="Line Chart")
tab8 = dbc.Tab([dcc.Graph(id="px_pie")], label="Pie Chart")
tab_9 = dbc.Tab([table], label="Table", className="p-4")
tabs10 = dbc.Card(dbc.Tabs([tab7, tab_9]))
tabs_11 = dbc.Card(dbc.Tabs([tab8]))

# ===========================================================================================================================================


# DROPDOWN
dropdown = html.Div(
    [
        dbc.Label("Filtrer les produits"),
        dcc.Dropdown(
            [{"label": html.Span([x], style={'color': 'Blue'}), "value": x} for x in products], value=products,
            id="produit",
            clearable=True,
            multi=True
        ),
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# CHECKLIST
checklist = html.Div(
    [
        dbc.Label("Pays"),
        dbc.Checklist(
            id="lands",
            options=[{"label": i, "value": i} for i in continents],
            value=continents,
            inline=True,
        ),
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# SLIDER
slider = html.Div(
    [
        dbc.Label("Filtrer les années"),
        dcc.RangeSlider(
            an[0],
            an[-1],
            1,
            id="ans",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[an[0], an[-1]],
            className="p-0",
        ),
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# LES CONTRÔLES
controls = dbc.Card(
    [slider, dropdown, checklist],
    body=True,
    style={"margin-top": "5%", "width": "80%"}
)

# ===========================================================================================================================================

layout2 = dbc.Row(
    [
        dbc.Col(
            [
                tabs10
            ],
            style={"height": "70%", "width": "40%", "display": "inline-block"}
        ),
        dbc.Col(
            [
                tabs_11
            ],
            style={"height": "70%", "width": "40%", "display": "inline-block"}
        ),
        dbc.Row(
            [
                controls
            ],
            style={"height": "15%", "width": "100%"}
        ),
    ],
    style=styles.CONTENT_STYLE
)


@callback(
    Output("line-chart_p2", "figure"),
    Output("px_pie", "figure"),
    Output("table_p2", "data"),
    Input("produit", "value"),
    Input("lands", "value"),
    Input("ans", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_line_chart(produits, lands, ans, theme):
    dff = df.copy(deep=True)
    dff = dff.loc[(dff["Produit"].isin(produits)) & (dff["mp_year"].astype(int).between(int(ans[0]), int(ans[-1]))) & (dff["Pays"].isin(lands))]
    data3 = dff.to_dict("records")

    fig3 = px.line(
        dff,
        x=dff.groupby("mp_year")["price_norm"].mean().keys(),
        y=dff.groupby("mp_year")["price_norm"].mean().values,
        template=template_from_url(theme)
    )

    fig3.update_layout(
        xaxis_title="Dates",
        yaxis_title="Fluctuations des prix"
    )
    dff = pd.DataFrame(dff.groupby("Pays")["price_norm"].mean().sort_values(ascending=False).head(6))
    fig_scatter3 = px.pie(dff, names=dff.index, values="price_norm", template=template_from_url(theme))

    return fig3, fig_scatter3, data3
