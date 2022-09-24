from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

df = pd.read_csv(
    'probability_of_death_global.csv'
)

sorted_age_groups = [
    '<1 year',
    '1 to 4',
    '5 to 9',
    '10 to 14',
    '15 to 19',
    '20 to 24'
    '25 to 29',
    '30 to 34',
    '35 to 39',
    '40 to 44',
    '45 to 49',
    '50 to 54',
    '55 to 59',
    '60 to 64',
    '65 to 69',
    '70 to 74',
    '75 to 79',
    '80 to 84',
    '85 to 89',
    '90 to 94',
    '95 to 99',
    '100 to 104',
    '105 to 109',
    '110 plus'
]

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# create filters
controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Sex"),
                dcc.Dropdown(
                    id="sex",
                    options=df['sex_name'].unique(),
                    value="both",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Location"),
                dcc.Dropdown(
                    id="location",
                    options=df['location_name'].unique(),
                    value="Global",
                    searchable=True,
                ),
            ]
        ),
    ],
    body=True,
)


# setup layout
app.layout = dbc.Container(
    [
        html.Br(),
        html.H1(
            children='Probability of death in world countries by sex and age groups dynamic from 1950 to 2019 years'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            children='Choose options'
                        ),
                        controls
                    ],
                    md=3,
                    align='center'
                ),
                dbc.Col(
                    dcc.Graph(
                        id="probability_of_death_graph",
                        config={
                        'displayModeBar': False
                        }
                    ),
                    md=9,
                )
            ],
            align="center",
        ),       
    ]

)

# setup the callback function
@app.callback(
    Output(component_id='probability_of_death_graph', component_property='figure'),
    Input(component_id='location', component_property='value'),
    Input(component_id='sex', component_property='value')
)

def update_graph(geo, sex):

    df_filtered = df.query(
        'location_name == @geo'
        ' and sex_name == @sex'
    ).sort_values(by='year_id')

    fig = make_subplots()

    for age_group_name in sorted_age_groups:
        fig.add_trace(
            go.Bar(
                x=df_filtered.query('age_group_name == @age_group_name')['year_id'],
                y=df_filtered.query('age_group_name == @age_group_name')['val'],
                name=age_group_name
            )
        )
    fig.update_layout(
        barmode='stack',
        template='plotly_white',
        height=500
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)