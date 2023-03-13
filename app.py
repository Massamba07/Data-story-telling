from dash import Dash, dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import pages as pa

# INIT
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], title="Ynov Data Science Project")
app = dash_app.server

# ===========================================================================================================================================

# HEADER
header = html.H4(
    "Data Storytelling : GBE - GUEYE - KARAYANNIDIS",
    className="text-white p-2 mb-2 text-center",
    style=pa.HEADER_STYLE
)

# ===========================================================================================================================================


# SIDEBAR
sidebar = html.Div(
    [
        html.H2("Sommaire", className="display-4"),
        html.Hr(),
        html.P(
            "Expliquer les fluctuations des prix de l'alimentaire", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Pertes alimentaires", href="/", active="exact"),
                dbc.NavLink("Pays", href="/page-2", active="exact"),
                dbc.NavLink("Prix de consommation", href="/page-3", active="exact"),
                dbc.NavLink("Prix de production", href="/page-4", active="exact"),
                dbc.NavLink("Page 4", href="/page-5", active="exact"),
                dbc.NavLink("Page 5", href="/page-6", active="exact"),
                dbc.NavLink("Page 6", href="/page-7", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"justify-content": "space-evenly"}
        ),
        html.Hr(),
        html.Img(
            src="https://imgs.search.brave.com/b_218gQQ1bSwOLEcJh_-Uaub-PKt8qVzOZQzN0nYKrY/rs:fit:381:150:1/g:ce"
                "/aHR0cHM6Ly93d3cu/eW5vdi1haXguZnIv/d3AtY29udGVudC91/cGxvYWRzLzIwMTcv/MDUvTG9nby1Zbm92"
                "/LUFpeC0xNTBweC5w/bmc",
            width="70%",
            style={"margin": "auto"}),
        html.Hr(),
        ThemeChangerAIO(aio_id="theme",
                        radio_props={"value": dbc.themes.QUARTZ},
                        button_props={"children": "Changer le thème"},
                        offcanvas_props={"title": "Choisir un thème"})
    ],
    style=pa.SIDEBAR_STYLE
)

# LE LAYOUT
dash_app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        header,
        dbc.Col(
            sidebar,
            style={"width": "13%"}
        ),
        html.Div(
            id='page-content'
        ),
    ],
    fluid=True,
    className="dbc", style={"height": "50%"}
)


# ===========================================================================================================================================

# PAGES
@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return pa.layout1
    elif pathname == '/page-2':
        return pa.layout2
    elif pathname == '/page-3':
        return pa.layout3
    elif pathname == '/page-4':
        return pa.layout6
    elif pathname == '/page-5':
        return pa.layout4
    elif pathname == '/page-6':
        return pa.layout5
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(
                f"Le chemin {pathname} n'existe pas...",
                style={
                    "color": "red",
                    "text-align": "center"
                }
            ),
            html.Hr(),
            html.Img(
                src="https://media.tenor.com/tL4TpMpm7DsAAAAM/sajna-sad.gif",
                style=pa.IMG_404
            )
        ],
        className="p-3 bg-light rounded-3",
        style=pa.CONTENT_STYLE
    )


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
