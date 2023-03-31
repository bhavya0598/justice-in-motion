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
import data_adult
from dash.dependencies import Input, Output
from controls import geo_list, year_list

df = px.data.gapminder()
geos = geo_list()
alberta = geos[0]
years = year_list()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
template = "flatly"
# theme changer button
theme_changer = html.Div(ThemeChangerAIO(aio_id="theme"), className="mb-4")

# header
header = dbc.Row(
    dbc.Col(
        html.Strong("Justice in Motion - A Visualization of Canadian Criminal Cases"),
    ),
    className="bg-danger text-white p-2 mb-5 text-center display-6 shadow-lg",
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
            id="provinces",
            options=[{"label": i, "value": i} for i in geos],
            value=[alberta],
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
            id="years",
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

# radio items for youth tab only (incarceration vs probation)
radio = html.Div(
    dcc.RadioItems(["Incarceration", "Probation"], "Incarceration", inline=True),
    className="mb-4",
)

# radio items for youth tab only (male vs female)
radio2 = html.Div(
    dcc.RadioItems(["Male", "Female"], "Female", inline=True), className="mb-4"
)

# youth figures


# adult figures


# tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(
            [dbc.Row(id="youth-figures")],
            # [
            #     dbc.Row(
            #         [dcc.Graph(figure=fig, className="m-4") for fig in youth_figures],
            #     )
            # ],
            label="Youth",
            tab_id="youth",
        ),
        dbc.Tab(
            [dbc.Row(id="adult-figures")],
            # [
            #     dbc.Row(
            #         [dcc.Graph(figure=fig, className="m-4") for fig in adult_figures]
            #     ),
            # ],
            label="Adult",
            tab_id="adult",
        ),
        dbc.Tab(label="Misc", tab_id="misc"),
    ],
    id="tabs",
    active_tab="youth",
)

# app layout
app.layout = html.Div(
    [
        dbc.Container(header, fluid=True, className="dbc"),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            controls,
                            width=3,
                        ),
                        dbc.Col(tabs, width=9, className="custom-scrollbar px-4"),
                    ],
                ),
                # dbc.Row(
                #     [dcc.Graph(figure=fig, className="m-4") for fig in youth_figures],
                # ),
                # dbc.Row([dcc.Graph(figure=fig, className="m-4") for fig in adult_figures]),
            ],
            fluid=False,
            className="dbc",
        ),
    ]
)

# callback for tabs
@app.callback(
    Output("youth-figures", "children"),
    Output("adult-figures", "children"),
    Input("tabs", "active_tab"),
    Input("years", "value"),
    Input("provinces", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def render_tab_content(active_tab, years, provinces, theme):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    print(active_tab, years, provinces, theme)
    start_year = years[0]
    end_year = years[1]
    if active_tab is not None:
        # figures for youth tab
        fig1 = data_youth.youth_indigenous_vs_nonindigenous(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig2 = data_youth.youth_commencing_correctional_services(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig3 = data_youth.youth_admissions_and_releases_to_correctional_services(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig4 = data_youth.youth_in_correctional_services_trend_3d(
            template_from_url(theme), "Incarceration", provinces
        )
        # fig5 = data_youth.youth_gender_trends_and_pie(
        #     start_year, end_year, template_from_url(theme), provinces
        # )
        fig6 = data_youth.youth_age_by_geo(
            start_year, end_year, template_from_url(theme), provinces
        )
        youth_figures = [fig1, fig2, fig3, fig4, fig6]

        # figures for adult tab
        fig7 = data_adult.adult_admissions_3dtrend(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig8 = data_adult.adult_custody_admissions_age_group(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig9 = data_adult.adult_custody_gender_heatmap(
            "Female", start_year, end_year, template_from_url(theme), provinces
        )
        fig10 = data_adult.adult_indigenous_vs_nonindigenous(
            start_year, end_year, template_from_url(theme), provinces
        )
        fig11 = data_adult.adult_sentence_length_by_sex(
            start_year, end_year, template_from_url(theme), provinces
        )
        adult_figures = [fig7, fig8, fig9, fig10, fig11]
        if active_tab == "youth":
            return [dcc.Graph(figure=fig, className="m-4") for fig in youth_figures], [
                dcc.Graph(figure=fig, className="m-4") for fig in adult_figures
            ]
        elif active_tab == "adult":
            return [dcc.Graph(figure=fig, className="m-4") for fig in youth_figures], [
                dcc.Graph(figure=fig, className="m-4") for fig in adult_figures
            ]
        elif active_tab == "misc":
            return
    return "no tabs selected"


if __name__ == "__main__":
    app.run_server(debug=True)
