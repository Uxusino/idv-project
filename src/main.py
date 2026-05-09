import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx
from preprocess import get_law_data, sum_laws, question_results, get_questions, SURVEYS

LAW_DF = get_law_data()
COLORS = ["#FF9A56", "#26CEAA", "#D60270", "#0038A8", "#5BCEFA"]

app = Dash(__name__)

app.layout = html.Div([
    html.H2(
        children='LGBTQ+ protection laws in EU countries and discrimination faced by the members of the community',
        style={
            'textAlign': 'center'
        }),
    html.Div(
        [
            html.Div(
                [
                    html.P("Select protection laws:",
                           title="If a law is in force, it adds +2 to the sum; laws applied partially add +1\nHover over a law to learn more details",
                           style={
                               "cursor": "help",
                               "textDecoration": "underline dotted"
                           }),
                    dcc.Checklist(
                        options=[
                            {
                                'label': html.Span(
                                    'Constitutional protection',
                                    title="Constitution explicitly includes sexual orientation and gender identity into their non-discrimination clauses"
                                ),
                                'value': 'CONST.'
                            },
                            {
                                'label': html.Span(
                                    'Broad Protection',
                                    title="Legal protections against discrimination in multiple domains"
                                ),
                                'value': 'BROAD PROT.'
                            },
                            {
                                'label': html.Span(
                                    'Employment',
                                    title="Legal protections against dicrimination in employment"
                                ),
                                'value': 'EMPLOY.'
                            },
                            {
                                'label': html.Span(
                                    'Hate crime',
                                    title="Regulations on criminal liability for crimes committed on the basis of the victim's sexual orientation or gender identity"
                                ),
                                'value': 'HATE CRIME'
                            },
                            {
                                'label': html.Span(
                                    'Incitement',
                                    title="Prohibition of incitement to violence, hatred or discrimination"
                                ),
                                'value': 'INCITEMENT'
                            },
                            {
                                'label': html.Span(
                                    'Conversion therapies banned',
                                    title="Regulation of harmful practices aimed to modify a person's sexual orientation, gender identity or gender expression"
                                ),
                                'value': 'BAN CONV. THERAPIES'
                            },
                            {
                                'label': html.Span(
                                    'Same-sex marriage',
                                    title="Legalization of same-sex marriage on an equal footing as heterosexual couples"
                                ),
                                'value': 'SAME SEX MARRIAGE'
                            },
                            {
                                'label': html.Span(
                                    'Civil unions',
                                    title="Legalization of same-sex partnership recognition in a form of a civil union"
                                ),
                                'value': 'CIVIL UNIONS'
                            },
                            {
                                'label': html.Span(
                                    'Joint adoption',
                                    title="Legalization of a process that allows a same-sex couple to adopt a child together"
                                ),
                                'value': 'JOINT ADOPTION'
                            },
                            {
                                'label': html.Span(
                                    'Second parent adoption',
                                    title="Legalization of a process that allows a person to adopt the child of their same-sex partner"
                                ),
                                'value': 'SECOND PARENT ADOPTION'
                            },
                        ],
                        value=['CONST.', 'BROAD PROT.', 'EMPLOY.', 'HATE CRIME', 'INCITEMENT',
                            'BAN CONV. THERAPIES', 'SAME SEX MARRIAGE', 'CIVIL UNIONS',
                            'JOINT ADOPTION', 'SECOND PARENT ADOPTION'],
                        id="checklist",
                    ),
                    dcc.Button("Select all", id="select-all", n_clicks=0, style={"margin": 2}),
                    dcc.Button("Clear all", id="clear-all", n_clicks=0, style={"margin": 2})
                ],
            style={
                'padding': 10,
            }
        ),
        html.Div(
            [
                dcc.Graph(
                    id="graph",
                    config={"displayModeBar": False},
                    clear_on_unhover=True,
                    responsive=False
                )
            ],
            style={
                'padding': 10
            }
        ),
        html.Div(
            [
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
                html.Pre(id="bars_0"),
                dcc.Markdown('''
                    ### References
                    [Sexual Orientation Laws in the World](https://www.kaggle.com/datasets/mpwolke/cusersmarildownloadsomophobiacsv) by Marília Prata, 2021
                    
                    [EU LGBT Survey](https://www.kaggle.com/datasets/ruslankl/european-union-lgbt-survey-2012?select=LGBT_Survey_DailyLife.csv) by Ruslan Klymentiev, 2012
                             
                    [ILGA World maps](https://ilga.org/ilga-world-maps/)
                '''),
            ],
            style={
                "padding": 10
            }
        ),
        
        ],
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'position': 'fixed'
        }
    ),
    
    ],
    style={
        'fontFamily': 'Arial'
    }
)

@app.callback(
    Output("checklist", "value"),
    Input("select-all", "n_clicks"),
    Input("clear-all", "n_clicks"),
    prevent_initial_call=True
)
def select_or_clear(select_btn, clear_btn):
    check = []
    if "select-all" == ctx.triggered_id:
        check = ['CONST.', 'BROAD PROT.', 'EMPLOY.', 'HATE CRIME', 'INCITEMENT',
                'BAN CONV. THERAPIES', 'SAME SEX MARRIAGE', 'CIVIL UNIONS',
                'JOINT ADOPTION', 'SECOND PARENT ADOPTION']
    elif "clear-all" == ctx.triggered_id:
        check = []
    return check


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
    fig.layout.height = 800
    fig.layout.width = 800
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
                  color_discrete_sequence=COLORS,
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