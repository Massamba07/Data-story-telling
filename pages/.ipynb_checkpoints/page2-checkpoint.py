from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from pages import gen
from pages import styles

df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

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
    [dropdown, slider],
    body=True,
    style={"margin-top":"5%"}
)

# ===========================================================================================================================================

tabs = dbc.Card(dbc.Tabs([
            dbc.Tab([
                dcc.Graph(
                figure=px.violin(
                    df, y="lifeExp", box=True, points="all")
                              )], 
                    label="Violin Plot"),
            dbc.Tab([
                gen.creating_grph(
                    "table", df, cols=["country", "continent"])
            ],
                    label="Table")
    ])
)

layout2 = dbc.Row(
    dbc.Col(
        [
            tabs,
            controls
    ],
        style={"width":"40%"}),
    style=styles.CONTENT_STYLE
)


#@callback(
#    Output("violin-plot1", "figure"),
#    Output("table", "data"),
#    Input("indicator", "value"),
#    Input("years", "value"),
#    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
#)

#def update_violin_chart(indicator, yrs, theme):
#    if continent == [] or indicator is None:
#        return {}, {}, []

#    dff = df[df.year.between(yrs[0], yrs[1])]
#    dff = dff[dff["continent"].isin(continent)]
#    data = dff.to_dict("records")
        
#    fig = px.violin(
#        dff,
#        y=indicator,
#        box=True,
#        points="all",
#        template=template_from_url(theme)
#    )
    
#    fig.update_layout(
#        xaxis_title="XLABEL", 
#        yaxis_title="YLABEL",
#    )
    
#    return fig, fig_scatter, data