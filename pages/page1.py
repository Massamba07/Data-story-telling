from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import styles
import pandas as pd
import numpy as np
from pages import gen

df = pd.read_csv("./datasets/food_loss_2000-2022.csv", index_col=0)
years = np.sort(df.annee.unique())
continents = df.pays.unique()
supply = df.food_supply_stage.unique()
data_food_price = pd.read_csv("./datasets/Food_price.csv", index_col=0)
data_fao_cons = pd.read_csv("./datasets/FAOSTAT_prix_conso.csv", index_col=0)
data_wfp = pd.read_csv("./datasets/wfp_foodprices_norm_clean.csv", index_col=0)
ds1 = pd.read_csv("./datasets/FAOSTAT_prix_prod.csv", index_col=0)

# SIMPLE TABLE
table = html.Div(
    dash_table.DataTable(
        id="table",
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

table2 = html.Div(
    dash_table.DataTable(
        id="table_prix",
        columns=[{"name": i, "id": i, "deletable": True} for i in ds1.columns],
        data=ds1.to_dict("records"),
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
tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart pertes")
tab2 = dbc.Tab([dcc.Graph(id="bar-chart")], label="Bar Chart 5 tops")
tab_3 = dbc.Tab([table], label="Table Pertes", className="p-4")
tab_x = dbc.Tab([dcc.Graph(id="pays_bar")], label="Top Pertes Pays")
tab4 = dbc.Tab([dcc.Graph(id="line")], label="Line Chart prix")
tab_5 = dbc.Tab([table2], label="Table Prix", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab_3, tab_x]))
tabs_2 = dbc.Card(dbc.Tabs([tab2, tab4, tab_5]))

# ===========================================================================================================================================


# DROPDOWN
dropdown = html.Div(
    [
        dbc.Label("Filtrer les pays"),
        dcc.Dropdown(
            [{"label": html.Span([x], style={'color': 'Blue'}), "value": x} for x in continents], value=continents,
            id="land",
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
        dbc.Label("Sélecteur d'étape du cycle de vie du produit"),
        dbc.Checklist(
            id="step_cycle",
            options=[{"label": i, "value": i} for i in supply],
            value=supply,
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
            years[0],
            years[-1],
            1,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[0], years[-1]],
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

layout1 = dbc.Row(
    [
        dbc.Col(
            [
                tabs
            ],
            style={"height": "70%", "width": "40%", "display": "inline-block"}
        ),
        dbc.Col(
            [
                tabs_2
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
    Output("line-chart", "figure"),
    Output("bar-chart", "figure"),
    Output("line", "figure"),
    Output("pays_bar", "figure"),
    Output("table", "data"),
    Input("step_cycle", "value"),
    Input("land", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_line_chart(step_cycle, land, years, theme):
    dff = df.copy(deep=True)
    dff = dff.loc[(dff["food_supply_stage"].isin(step_cycle)) & (dff["annee"].between(years[0], years[-1])) & (dff["pays"].isin(land))]
    data = dff.to_dict("records")
    ds1f = ds1[ds1["Zone"].isin(continents)]
    ds1f = ds1f.loc[(ds1f["Année"].between(years[0], years[-1]) & (ds1f["Zone"].isin(land)))]

    fig = px.line(
        dff,
        x=dff.groupby("annee")["perte_pourcentage"].mean().keys(),
        y=dff.groupby("annee")["perte_pourcentage"].mean().values,
        template=template_from_url(theme)
    )

    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="Pertes moyennes en %"
    )

    fig_scatter = px.bar(
        dff,
        x=dff["cause_of_loss"].value_counts().head(5).keys(),
        y=dff["cause_of_loss"].value_counts().head(5).values,
        orientation="v",
        template=template_from_url(theme)
    )

    fig_scatter.update_layout(
        xaxis_title="Causes",
        yaxis_title="Pertes (%)"
    )

    fig2 = px.line(
        ds1f,
        x=ds1f.Année.unique(),
        y=ds1f.groupby("Année")["norm_price"].mean(),
        template=template_from_url(theme)
    )

    fig2.update_layout(
        xaxis_title="Dates",
        yaxis_title="Prix normalisés"
    )

    fig_scatter_pays = px.bar(
        dff.groupby("pays")["perte_pourcentage"].mean(),
        x=dff.sort_values(["perte_pourcentage", "pays"]).groupby("pays")["perte_pourcentage"].mean().nlargest(5).keys(),
        y=dff.sort_values(["perte_pourcentage", "pays"]).groupby("pays")["perte_pourcentage"].mean().nlargest(5).values,
        orientation="v",
        template=template_from_url(theme)
    )

    fig_scatter_pays.update_layout(
        xaxis_title="Pays",
        yaxis_title="Pertes moyennes (%)"
    )

    return fig, fig_scatter, fig2, fig_scatter_pays, data
