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
from dash.dependencies import Input, Output, State
from controls import geo_list, year_list
import plotly.graph_objs as go

df = px.data.gapminder()
geos = geo_list()
allprovince = [geos[0]]
years = year_list()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# theme changer button
theme_changer = html.Div(ThemeChangerAIO(aio_id="theme"), className="mb-4")

# loading spinner
spinner = dbc.Spinner(
    size="md",
    color="info",
    type="grow",
    fullscreen=False,
    show_initially=False,
    spinnerClassName="d-none",
    id="spinner",
    children=[html.Div(id="output")],
)


# update alert
alert = html.Div(
    dbc.Alert(
        "Updating...",
        id="alert-auto",
        is_open=False,
        duration=1500,
        dismissable=True,
        fade=True,
        class_name="alert alert-primary",
    ),
    className="custom-alert",
)

# header
header = dbc.Row(
    dbc.Col(
        html.Strong("Justice in Motion - A Visualization of Canadian Criminal Cases"),
    ),
    className="bg-danger text-white p-2 mb-5 text-center display-6 shadow-lg",
)

# provinces checklist
checklist = html.Div(
    [
        dbc.Label("Select Provinces:"),
        dbc.Checklist(
            id="provinces",
            options=[{"label": i, "value": i} for i in geos],
            value=allprovince,
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
            tooltip={"always_visible": False, "placement": "topLeft"},
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
    dcc.RadioItems(
        options=[
            {
                "label": "Incarceration",
                "value": "Incarceration",
            },
            {
                "label": "Probation",
                "value": "Probation",
            },
        ],
        value="Incarceration",
        inline=True,
        id="radio",
        inputClassName="mx-2 form-check-input",
    ),
    className="mt-4",
)

# radio items for youth tab only (male vs female)
radio2 = html.Div(
    dcc.RadioItems(
        options=[
            {
                "label": "Male",
                "value": "Male",
            },
            {
                "label": "Female",
                "value": "Female",
            },
        ],
        value="Female",
        inline=True,
        id="radio2",
        inputClassName="mx-2 form-check-input",
    ),
)

# tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(
            [dbc.Row(id="adult-figures")],
            label="Adult",
            tab_id="adult",
        ),
        dbc.Tab(
            [dbc.Row(id="youth-figures")],
            label="Youth",
            tab_id="youth",
        ),
    ],
    id="tabs",
    active_tab="adult",
)

# app layout
app.layout = html.Div(
    [
        dbc.Container(header, fluid=True, className="dbc"),
        dbc.Container(
            [
                alert,
                dbc.Row(
                    [
                        dbc.Col(
                            controls,
                            width=2,
                        ),
                        dbc.Col(tabs, width=10, className="custom-scrollbar px-4"),
                    ],
                ),
                dbc.Row(
                    [
                        radio,
                        radio2,
                        dcc.Graph(id="fig4", className="m-4"),
                        dcc.Graph(id="fig9", className="m-4"),
                        dcc.Graph(id="fig12", className="m-4"),
                    ],
                    className="d-none",
                ),
            ],
            fluid=True,
            className="dbc",
        ),
    ]
)

# callback to disable provinces checklist when allprovinces is selected
@app.callback(
    Output("provinces", "options"),
    Input("provinces", "value"),
    State("provinces", "options"),
)
def update_checklist(selected_value, options):
    if allprovince[0] in selected_value:
        # Disable all options except the first one
        new_options = []
        new_options.append(options[0])
        for option in options[1:]:
            new_option = option.copy()
            new_option["disabled"] = True
            new_options.append(new_option)
        return new_options
    else:
        # Enable all options
        for option in options:
            option["disabled"] = False
        return options


# callback for slider
@app.callback(
    Output("years", "min"),
    Input("tabs", "active_tab"),
)
def update_slider_min(active_tab):
    if active_tab == "youth":
        return 1997
    return 2000


# callback for alert
@app.callback(
    Output("alert-auto", "is_open"),
    Input("years", "value"),
    Input("provinces", "value"),
    [State("alert-auto", "is_open")],
)
def toggle_alert(years, provinces, is_open):
    if years is not None and provinces is not None:
        return not is_open
    return is_open


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
    start_year = years[0]
    end_year = years[1]
    if allprovince[0] in provinces:
        provinces = allprovince
    if active_tab is not None and len(provinces) != 0 and years is not None:
        if active_tab == "youth":
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
            fig5 = data_youth.youth_gender_trends_and_pie(
                start_year, end_year, template_from_url(theme), provinces
            )
            fig6 = data_youth.youth_age_by_geo(
                start_year, end_year, template_from_url(theme), provinces
            )
            youth_graphs = [
                radio,
                dcc.Graph(id="fig4", className="m-4"),
                dcc.Graph(figure=fig1, className="m-4"),
                dcc.Graph(figure=fig2, className="m-4"),
                dcc.Graph(figure=fig3, className="m-4"),
                dcc.Graph(figure=fig5, className="m-4"),
                dcc.Graph(figure=fig6, className="m-4"),
            ]
            years = year_list()
            return (youth_graphs, [])

        elif active_tab == "adult":
            # figures for adult tab
            fig7 = data_adult.adult_admissions_3dtrend(
                start_year, end_year, template_from_url(theme), provinces
            )
            fig8 = data_adult.adult_custody_admissions_age_group(
                start_year, end_year, template_from_url(theme), provinces
            )
            fig10 = data_adult.adult_indigenous_vs_nonindigenous(
                start_year, end_year, template_from_url(theme), provinces
            )
            fig11 = data_adult.adult_sentence_length_by_sex(
                start_year, end_year, template_from_url(theme), provinces
            )

            adult_graphs = [
                radio,
                dcc.Graph(id="fig12", className="m-4"),
                dcc.Graph(figure=fig7, className="m-4"),
                dcc.Graph(figure=fig8, className="m-4"),
                radio2,
                dcc.Graph(id="fig9", className="m-4"),
                dcc.Graph(figure=fig10, className="m-4"),
                dcc.Graph(figure=fig11, className="m-4"),
            ]
            return ([], adult_graphs)
    return [], []


# callback for radio youth
@app.callback(
    Output("fig4", "figure"),
    Input("tabs", "active_tab"),
    Input("radio", "value"),
    Input("provinces", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_radio(active_tabs, value, provinces, years, theme):
    if active_tabs == "youth":
        fig = data_youth.youth_in_correctional_services_trend_3d(
            years[0], years[-1], template_from_url(theme), value, provinces
        )
        return fig


# callback for radio adult
@app.callback(
    Output("fig12", "figure"),
    Input("tabs", "active_tab"),
    Input("radio", "value"),
    Input("provinces", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_radio(active_tabs, value, provinces, years, theme):
    if active_tabs == "adult":
        fig = data_adult.adults_rates_geomap(
            years[0], years[-1], template_from_url(theme), value
        )
        return fig


# callback for radio2
@app.callback(
    Output("fig9", "figure"),
    Input("radio2", "value"),
    Input("provinces", "value"),
    Input("years", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_radio2(value, provinces, years, theme):
    fig = data_adult.adult_custody_gender_heatmap(
        value, years[0], years[-1], template_from_url(theme), provinces
    )
    return fig


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
