"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import (
    ThemeChangerAIO,
    template_from_url,
    load_figure_template,
)
import plotly.express as px
import data_youth
from controls import geo_list, year_list

df = px.data.gapminder()
geos = geo_list()
alberta = geos[0]
years = year_list()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# theme changer button
theme_changer = html.Div(ThemeChangerAIO(aio_id="theme"), className="mb-4")

# header
header = dbc.Row(
    dbc.Col(
        html.Strong("Justice in Motion - A Visualization of Canadian Criminal Cases"),
    ),
    className="bg-danger text-white p-2 mb-5 text-center display-5 shadow-lg",
)

# provinces dropdown
# dropdown = html.Div(
#     [
#         dbc.Label("Select provinces:"),
#         dcc.Dropdown(geos, [alberta], id="indicator", clearable=False, multi=True),
#     ],
#     className="mb-4",
# )

# provinces checklist
checklist = html.Div(
    [
        dbc.Label("Select Provinces:"),
        dbc.Checklist(
            id="continents",
            options=[{"label": i, "value": i} for i in geos],
            value=alberta,
            inline=False,
        ),
    ],
    className="mb-4",
)

# years slider
marks = {year: str(year) for year in range(years[0], years[-1] + 1, 5)}
slider = html.Div(
    [
        dbc.Label("Select Years:"),
        dcc.RangeSlider(
            id="year-slider",
            min=years[0],
            max=years[-1],
            step=1,
            value=[years[0], years[-1]],
            marks=marks,
        ),
    ],
    className="mb-4",
)

# controls
controls = dbc.Card(
    [checklist, slider, theme_changer],
    body=True,
)

# tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(label="Youth", tab_id="youth"),
        dbc.Tab(label="Adult", tab_id="adult"),
        dbc.Tab(label="Misc", tab_id="misc"),
    ],
    id="tabs",
    active_tab="youth",
)

# figures
fig2 = data_youth.youth_commencing_correctional_services(years[0], years[-1], [alberta])
fig3 = data_youth.youth_admissions_and_releases_to_correctional_services(
    years[0], years[-1], [alberta]
)
fig4 = data_youth.youth_in_correctional_services_trend_3d("Incarceration")
fig5 = data_youth.youth_gender_trends_and_pie(1997, 2005)
fig6 = data_youth.youth_age_by_geo(years[0], years[-1], [alberta])
fig7 = data_youth.youth_indigenous_vs_nonindigenous(1999, 2005)
figures = [fig2, fig3, fig4, fig5, fig6, fig7]

# app layout
app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [dbc.Col(controls, width=3), dbc.Col(tabs, width=9)],
        ),
        # [dcc.Graph(figure=fig, className="m-4") for fig in figures],
    ],
    fluid=True,
    className="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=True)
