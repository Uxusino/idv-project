import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx
from preprocess import get_law_data, sum_laws, question_results, get_questions, SURVEYS

LAW_DF = get_law_data()

app = Dash(__name__)

app.layout = html.Div([
    html.H4(
        children='LGBTQ+ protection laws in European countries and discrimination faced by the members of the community',
        style={
            'textAlign': 'center'
        }),
    html.Div(
        [html.Div(
            children=[
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
                    id="checklist",
                ),

            ],
            style={
                'padding': 10
            }
        ),
        html.Div(
            children = [
                dcc.Graph(
                    id="graph",
                    config={"displayModeBar": False},
                    clear_on_unhover=True
                )
            ],
            style={
                'padding': 10
            }
        ),
        html.Div(
            children=[
                html.P("Select survey:"),
                dcc.Dropdown(
                    options=SURVEYS,
                    value=next(iter(SURVEYS)),
                    id="dropdownSurvey"
                ),
                html.P("Select question:"),
                dcc.Dropdown(
                    id="dropdownQuestion"
                ),
                dcc.Store(id="selectedCountry", data=None),
                dcc.Graph(id="bars"),
                html.Pre(id="bars_0")
            ],
            style={
                "padding": 10
            }
        )],
        style={
            'display': 'flex',
            'flexDirection': 'row'
        }
    )
])

@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
)
def display_choropleth(law_values):
    df_sums = sum_laws(LAW_DF, law_values)
    fig = px.choropleth(df_sums, locations='COUNTRY',
                    locationmode='country names', color="Sum",
                    color_continuous_scale='Viridis',
                    range_color=(np.min(df_sums["Sum"]), np.max(df_sums["Sum"])),
                    scope="europe",
                    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, clickmode="event+select")
    fig.update_geos(
        scope="europe",
        resolution=50
    )

    return fig

@app.callback(
    Output("bars", "figure"),
    Output("selectedCountry", "data"),
    Input("graph", "selectedData"),
    Input("dropdownQuestion", "value"),
    Input("dropdownSurvey", "value"),
    State("selectedCountry", "data"),
    prevent_initial_call=True
)
def display_bars(selectedData, dropdown_question, dropdown_survey, current):

    if not selectedData:
        country = "Average"
    else:
        country = selectedData["points"][0]["location"]

    df_q = question_results(dropdown_survey, dropdown_question, country)

    bars = px.bar(df_q, x="answer", y="percentage",
                  title=country, color="subset",
                  barmode="group")
    return bars, country

@app.callback(
    Output("dropdownQuestion", "options"),
    Input("dropdownSurvey", "value")
)
def set_questions_options(dropdown_survey):
    return get_questions(dropdown_survey)

@app.callback(
    Output("dropdownQuestion", "value"),
    Input("dropdownQuestion", "options")
)
def set_questions_value(available_options: dict):
    return next(iter(available_options))

app.run(debug=True)