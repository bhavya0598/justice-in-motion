"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import data_youth

df = px.data.gapminder()
# fig1 = youth_custodial_and_community_supervision_trend('Alberta')
fig2 = data_youth.youth_commencing_correctional_services(
    1999, 2022, ["Alberta", "Nunavut"]
)
fig3 = data_youth.youth_admissions_and_releases_to_correctional_services(
    1999, 2005, ["Alberta", "Manitoba"]
)
fig4 = data_youth.youth_in_correctional_services_trend_3d("Incarceration")
fig5 = data_youth.youth_gender_trends_and_pie(1997, 2005)
figures = [fig5]

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

# figures = [
#     px.scatter(
#         df.query("year==2007"),
#         x="gdpPercap",
#         y="lifeExp",
#         size="pop",
#         color="continent",
#         log_x=True,
#         size_max=60,
#         template=template,
#         title="Gapminder 2007: '%s' theme" % template,
#     )
#     for template in templates
# ]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([dcc.Graph(figure=fig, className="m-4") for fig in figures])

if __name__ == "__main__":
    app.run_server(debug=True)
