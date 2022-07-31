# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:08:57 2022

@author: pmayaduque
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash import no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly import graph_objs as go


import pandas as pd
book_teachers_id = '1bqZ8OnYfpM0A6EoVoM_YRurfNmn2UCTAzPYdkZk2vaM'
book_lists_id = '17DTbRs54Y-7nntaSqaIFEHAcMNa4ven6OxDqWswT3rE'


url_teachers = f"https://docs.google.com/spreadsheets/d/{book_teachers_id}/gviz/tq?tqx=out:csv"
url_lists= f"https://docs.google.com/spreadsheets/d/{book_lists_id}/gviz/tq?tqx=out:csv"

df_teachers= pd.read_csv(url_teachers)
teachers_list = df_teachers["nombre"].values.tolist()
teachers_dict = {i:teachers_list[i] for i in  range(len(teachers_list))}
df_lists= pd.read_csv(url_lists)


# Define stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]

# Create the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title="IE Barrio salvador")
# needed to run in heroku
server = app.server

app.layout = dbc.Container([
        #navbar,
        dbc.Row("Hello"),
        dbc.Container(
            dbc.Card([
                    dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Card title", className="card-title"),
                            html.P(
                                "Some quick example text to build on the card title and "
                                "make up the bulk of the card's content.",
                                className="card-text",
                            ),
                            dcc.Dropdown(
                               options=['New York City', 'Montreal', 'San Francisco'],
                               value='Montreal'
                            ),
                            dbc.Button("Go somewhere", color="primary"),
                        ]
                    ),
            ]),
                      
                      
            fluid=True
        ),


        dbc.Container(id="tab-content", className="p-4", fluid=True),
        #dbc.Row(html.Img(src='assets/images/footnote_federica.png', style={'width':'100%'})),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
    


