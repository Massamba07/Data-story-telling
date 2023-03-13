from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import styles
from pages import gen

df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

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

# CHANGER L'AFFICHAGE DES TABS
tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab_3 = dbc.Tab([table], label="Table", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab_3]))
tabs_2 = dbc.Card(dbc.Tabs([tab2]))


# ===========================================================================================================================================


# DROPDOWN
dropdown = html.Div(
    [
        dbc.Label("Sélecteur de variable (y)"),
        dcc.Dropdown(
            [{"label":html.Span(['gdpPercap'], style={'color': 'Blue'}), "value":"gdpPercap"}, 
             {"label":html.Span(['lifeExp'], style={'color': 'Blue'}), "value":"lifeExp"}, 
             {"label":html.Span(['pop'], style={'color': 'Blue'}), "value":"pop"}],
            "pop",
            id="indicator",
            clearable=False,
        ),
    ],
    className="mb-4",
)

# ===========================================================================================================================================


# CHECKLIST
checklist = html.Div(
    [
        dbc.Label("Filtrer les continents"),
        dbc.Checklist(
            id="continents",
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
            years[0],
            years[-1],
            1,
            id="years",
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
    [dropdown, checklist, slider],
    body=True,
    style={"margin-top":"5%"}
)

# ===========================================================================================================================================

layout1 = dbc.Row(
            [
                dbc.Col(
                    [
                        tabs, controls
                    ],
                    style={"width":"40%"}
                       ),
                dbc.Col(
                    [
                        tabs_2
                    ],
                    style={"width":"40%"}
                ),
                
            ],
            style=styles.CONTENT_STYLE
        )

@callback(
    Output("line-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("table", "data"),
    Input("indicator", "value"),
    Input("continents", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)

def update_line_chart(indicator, continent, yrs, theme):
    if continent == [] or indicator is None:
        return {}, {}, []

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff["continent"].isin(continent)]
    data = dff.to_dict("records")
    
    fig = gen.creating_grph("line", dataframe=dff, x_axis="year", y_axis=indicator)
    
    fig.update_layout(
        xaxis_title="XLABEL", 
        yaxis_title="YLABEL",
        color="continent",
        line_group="country",
        template=template_from_url(theme)
    )
        
    fig_scatter = px.scatter(
        df.query(f"year=={yrs[1]} & continent=={continent}"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template=template_from_url(theme),
        title="Année %s" % (yrs[1])       
    )
    
    fig_scatter.update_layout(
        xaxis_title="XLABEL", 
        yaxis_title="YLABEL"
    )
    
    return fig, fig_scatter, data