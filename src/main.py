import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from preprocess import get_law_data, sum_laws

LAW_DF = get_law_data()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('LGBTQ+ protection laws in European countries'),
    html.P("Select protection laws:"),
    dcc.Checklist(
        options=[
            {'label': 'Broad Protection', 'value': 'BROAD PROT.'},
            {'label': 'Employment', 'value': 'EMPLOY.'},
            {'label': 'Hate Crime', 'value': 'HATE CRIME'},
            {'label': 'Incitement', 'value': 'INCITEMENT'},
            {'label': 'Conversion therapies banned', 'value': 'BAN CONV. THERAPIES'},
            {'label': 'Same sex marriage', 'value': 'SAME SEX MARRIAGE'},
            {'label': 'Civil unions', 'value': 'CIVIL UNIONS'},
            {'label': 'Joint adoption', 'value': 'JOINT ADOPTION'},
            {'label': 'Second parent adoption', 'value': 'SECOND PARENT ADOPTION'},
        ],
        value=['BROAD PROT.', 'EMPLOY.', 'HATE CRIME', 'INCITEMENT',
               'BAN CONV. THERAPIES', 'SAME SEX MARRIAGE', 'CIVIL UNIONS',
               'JOINT ADOPTION', 'SECOND PARENT ADOPTION'],
        id="checklist"
    ),
    dcc.Graph(id="graph")
])

@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value")
)
def display_choropleth(values):
    df_sums = sum_laws(LAW_DF, values)
    fig = px.choropleth(df_sums, locations='COUNTRY',
                    locationmode='country names', color="Sum",
                    color_continuous_scale='Viridis',
                    range_color=(np.min(df_sums["Sum"]), np.max(df_sums["Sum"])),
                    scope="europe",
                    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_geos(
        scope="europe",
        resolution=50
    )
    return fig

app.run(debug=True)