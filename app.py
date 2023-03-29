"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import data_youth
from list import geo_list, year_list

df = px.data.gapminder()
geos = geo_list()
years = year_list()
fig2 = data_youth.youth_commencing_correctional_services(
    1999, 2022, ["Alberta", "Nunavut"]
)
fig3 = data_youth.youth_admissions_and_releases_to_correctional_services(
    1999, 2005, ["Alberta", "Manitoba"]
)
fig4 = data_youth.youth_in_correctional_services_trend_3d("Incarceration")
fig5 = data_youth.youth_gender_trends_and_pie(1997, 2005)
fig6 = data_youth.youth_age_by_geo(
    1999, 2022, ["Ontario", "Alberta", "Manitoba", "Provinces and territories"]
)
fig7 = data_youth.youth_indigenous_vs_nonindigenous(1999, 2005)
figures = [fig2, fig3, fig4, fig5, fig6, fig7]

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Checklist(geos, [geos[0]], inputClassName="me-2"),
            )
        ),
        # [dcc.Graph(figure=fig, className="m-4") for fig in figures],
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
