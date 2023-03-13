from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import gen
from pages import styles
import pandas as pd

df = px.data.gapminder()
#df_prod=pd.read_csv("./datasets/wfp_foodprices_norm_clean.csv")
df_prod = pd.read_csv("./datasets/FAOSTAT_prix_prod.csv")
years = df_prod['Année'].unique()
prix = df_prod["norm_price"].unique()
# ===========================================================================================================================================

# SIMPLE TABLE
table = html.Div(
    dash_table.DataTable(
        id="table_5",
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


# DROPDOWNbvhbhb {"label":html.Span([i], style={'color': 'Blue'}), "value":i},
dropdown = html.Div(
    [
        dbc.Label("Sélecteur de variable (Prix d'approvisionnement) (y)"),
        dcc.Dropdown(id='dropdown_5', options=[{"label":html.Span(i, style={'color': 'Blue'}), "value":i} for i in df_prod['Zone'].unique()], multi=True, placeholder='Filter by the country...')
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# SLIDER
slider = html.Div(
    [
         html.H3(
            "Influence de la quantité des ventes", className="lead"
        ),
        html.Hr(),
        dbc.Label("Filtrer les années"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            1,
            id="years_5",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[4], years[-1]],
            className="p-0",
        ),
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# LES CONTRÔLES
controls = dbc.Card(
    [dropdown, slider],
    body=True,
    style={"margin-bottom":"5%"}
)

# ===========================================================================================================================================
tabs = dbc.Card(dbc.Tabs([
            dbc.Tab([dcc.Graph( figure=px.violin(
                    df_prod, y="norm_price", box=True,
                points='all'
            )
                              )], 
                    label="Violin Plot"),
            dbc.Tab([
                gen.creating_grph(
                    "table", df_prod, cols=["Zone", "Année", "norm_price"])
            ],
                    label="Table"),
            dbc.Tab([dcc.Graph(id="line-chart_4")], label="Line Chart")
    ])
)

layout5 = dbc.Row(
    dbc.Col(
        [
            controls,
            tabs
            
    ],
        style={"width":"40%"}),
    style=styles.CONTENT_STYLE
)


@callback(
    Output("line-chart_5", "figure"),
    Output("violin-plot1_2", "figure"),
    Output("table_5", "data"),
    Input("indicator", "value"),
    Input("prix", "value"),
    Input("years_5", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)

def update_violin_chart(indicator,prix, yrs, theme):
    if prix == [] or indicator is None:
        return {}, {}, []

    dff = df_prod[df_prod.year.between(yrs[0], yrs[1])]
    dff = dff[dff["price_norm"].isin(prix)]
    data = dff.to_dict("records")
        
    fig = px.violin(
        dff,
        y=indicator,
        box=True,
        points="all",
        template=template_from_url(theme)
    )
    
    fig.update_layout(
        xaxis_title="XLABEL", 
        yaxis_title="YLABEL",
    )
    
    fig_line = px.line(
        df_prod,
         x="year",
        y=indicator,
        color="continent",
        line_group="country",
        template=template_from_url(theme)
    )
    
    fig_line.update_layout(
        xaxis_title="XLABEL", 
        yaxis_title="YLABEL",
    )
    
    return fig, fig_line, data
