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
import pygsheets
import gspread
import pandas as pd
from datetime import date



import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('access_key.json', scopes=scopes)

gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


book_teachers_id = '1bqZ8OnYfpM0A6EoVoM_YRurfNmn2UCTAzPYdkZk2vaM'
book_teachers = gc.open_by_key(book_teachers_id)
worksheet = book_teachers.worksheet('Docentes')
#url_teachers = f"https://docs.google.com/spreadsheets/d/{book_teachers_id}/gviz/tq?tqx=out:csv"
#df_teachers= pd.read_csv(url_teachers)
df_teachers= pd.DataFrame(worksheet.get_all_records())
teachers_list = df_teachers["nombre"].values.tolist()
teachers_dict = [{"label": k, "value": k} for k in teachers_list]

book_classes_id = '17DTbRs54Y-7nntaSqaIFEHAcMNa4ven6OxDqWswT3rE'
book_classes = gc.open_by_key(book_classes_id)
worksheet = book_classes.worksheet('Cursos')
#url_classes= f"https://docs.google.com/spreadsheets/d/{book_classes}/gviz/tq?tqx=out:csv"
#df_classes= pd.read_csv(url_classes)
df_classes= pd.DataFrame(worksheet.get_all_records())
classes_id = df_classes["curso"].values.tolist()
classes_list = dict(zip(df_classes.curso, df_classes.google_id))
classes_dict = [{"label": k, "value": k} for k in classes_list.keys()]


# book_class1A = '1TtuUshmaQPrJa1C33v1pec4Cninh98xXqGIebbG9APs'
# #book_class1A = classes_dict[selec_class]
# sheet_estudiantes = 'Estudiantes'
# url_class1A = f"https://docs.google.com/spreadsheets/d/{book_class1A}/gviz/tq?tqx=out:csv&sheet={'Estudiantes'}"
# df_class1A= pd.read_csv(url_class1A)
# class1A_list = list(zip(df_class1A.codigo, df_class1A.nombre))
# class1A_dict = [{"label": k[1], "value": k[0]} for k in class1A_list]
    


# Define stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]


# #authorization
# gc = pygsheets.authorize(service_file='access_key.json')

# # Create empty dataframe
# df = pd.DataFrame()

# # Create a column
# df['name'] = ['John', 'Steve', 'Sarah']

# #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
# sh = gc.open('Asistencia')

# #select the first sheet 
# wks = sh[0]

# #update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(df,(3,2))

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
                            dcc.DatePickerSingle(
                                id='date-picker',
                                min_date_allowed=date(2022, 1, 1),
                                max_date_allowed=date(2032, 1, 1),
                                initial_visible_month=date(2022, 1, 1),
                                date=date.today()
                            ),
                            dcc.Dropdown(
                                id='drop_teachers',
                                options=teachers_dict,
                                value=teachers_list[0]
                            ),
                            dcc.Dropdown(
                                id='drop_class',
                                options=classes_dict,
                                value=classes_id[0]
                            ),
                            dbc.Button(
                                "Go somewhere",
                                id='button_save',
                                color="primary"),
                            dbc.Button(
                                "Show",
                                id='button_graph',
                                disabled = True,
                                color="primary"),
                        ]
                    ),
            ]),
                      
                      
            fluid=True
        ),
        dbc.Container(
            dcc.Checklist(
                id='check_students',
                #options=class1A_dict,
                style={"display":"block"},
                labelStyle={'display': 'block'},
                inputStyle={"margin-right": "20px"}
            ),
        ),
            
       

        dbc.Container(id="tab-content", className="p-4", fluid=True),
        #dbc.Row(html.Img(src='assets/images/footnote_federica.png', style={'width':'100%'})),
    ],
    fluid=True,
)




# Callback to update list of students
@app.callback(
    Output(component_id='check_students', component_property='options'),
    Output(component_id='check_students', component_property='value'),
    Input(component_id='drop_class', component_property='value')
    )
def update_list(selec_class):
    #book_class = classes_list[selec_class]
    #sheet_estudiantes = 'Estudiantes'
    #url_class = f"https://docs.google.com/spreadsheets/d/{book_class}/gviz/tq?tqx=out:csv&sheet={'Estudiantes'}"
    #df_class= pd.read_csv(url_class)
    book_class_id = classes_list[selec_class]
    sheet_estudiantes = 'Estudiantes'
    book_class = gc.open_by_key(book_class_id)
    worksheet = book_class.worksheet('Estudiantes')
    #url_class = f"https://docs.google.com/spreadsheets/d/{book_class}/gviz/tq?tqx=out:csv&sheet={'Estudiantes'}"
    #df_class= pd.read_csv(url_class)
    df_class = pd.DataFrame(worksheet.get_all_records())  
    class_list = list(zip(df_class.codigo, df_class.nombre))
    class_dict = [{"label": k[1], "value": k[1]} for k in class_list]
    
    return class_dict, list()

@app.callback(
    Output("button_graph", "disabled"),
    [Input("button_save", "n_clicks")],    
    [Input('drop_class', 'value')],
    [Input('date-picker', 'date')],
    [Input('drop_teachers', 'value')],
    [State("check_students", "value")], 
)
def do_something(trigger, selec_class, date_picked, teacher_name, values):
    if trigger:        
        book_class_id = classes_list[selec_class]
        sheet_estudiantes = 'Estudiantes'
        book_class = gc.open_by_key(book_class_id)
        worksheet = book_class.worksheet('Estudiantes')
        #url_class = f"https://docs.google.com/spreadsheets/d/{book_class}/gviz/tq?tqx=out:csv&sheet={'Estudiantes'}"
        #df_class= pd.read_csv(url_class)
        df_class = pd.DataFrame(worksheet.get_all_records())
        df = df_class[df_class['nombre'].isin(values)]
        df.insert(0, 'fecha', date_picked)
        df['curso'] = selec_class
        df['prof_reporta'] = teacher_name  
        #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
        #book = gc.open(selec_class)
        #select the first sheet 
        
        # dataframe (create or import it)
        df_values = df.values.tolist()
        gs = gc.open_by_key(book_class_id)
        gs.values_append('Faltas', {'valueInputOption': 'RAW'}, {'values': df_values})
        return False
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
    


