from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url


# Fonction pour retourner un graphe de différent type (line, violin, scatter ou table)
def creating_grph(the_type, dataframe, y_axis="", x_axis="", cols=None):
    if cols is None:
        cols = []
    if the_type == "violin":
        my_figure = px.violin(dataframe, y=y_axis, box=True, points="all")
    elif the_type == "line":
        my_figure = px.line(dataframe, y=y_axis, x=x_axis)
    elif the_type == "scatter":
        my_figure = px.scatter(dataframe, y=y_axis, x=x_axis)
    elif the_type == "table":
        my_figure = html.Div(
            dash_table.DataTable(
                columns=[{"name": i, "id": i, "deletable": True} for i in dataframe[cols].columns],
                data=dataframe[cols].to_dict("records"),
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
    return my_figure
