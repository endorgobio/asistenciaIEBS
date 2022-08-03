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
from plotly.offline import plot



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

# books ids
book_teachers_id = '1bqZ8OnYfpM0A6EoVoM_YRurfNmn2UCTAzPYdkZk2vaM'
book_classes_id = '17DTbRs54Y-7nntaSqaIFEHAcMNa4ven6OxDqWswT3rE'
book_consolidate_id = '1w8h3dzb4dqSGDrj_QThuES7J_aqrAx_nwXgY7qUDSA0'

book_teachers = gc.open_by_key(book_teachers_id)
worksheet = book_teachers.worksheet('Docentes')
#url_teachers = f"https://docs.google.com/spreadsheets/d/{book_teachers_id}/gviz/tq?tqx=out:csv"
#df_teachers= pd.read_csv(url_teachers)
df_teachers= pd.DataFrame(worksheet.get_all_records())
teachers_list = df_teachers["nombre"].values.tolist()
teachers_dict = [{"label": k, "value": k} for k in teachers_list]


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
    dbc.Container(
        dbc.Card([
            #dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
            dbc.CardBody([
                # html.H4("Card title", className="card-title"),
                html.P(
                    "Complete la información del curso al cual registrará la asistencia.",
                    className="card-text",
                ),
                dbc.Row([
                    dbc.Col(dbc.Label("Fecha"), md=4),
                    dbc.Col(
                        dcc.DatePickerSingle(
                            id='date-picker',
                            min_date_allowed=date(2022, 1, 1),
                            max_date_allowed=date(2032, 1, 1),
                            initial_visible_month=date(2022, 1, 1),
                            date=date.today()
                        ),
                        md=8
                    )
                    
                ]),     
                dbc.Row([
                    dbc.Col(dbc.Label("Docente"), md=4),
                    dbc.Col(
                        dcc.Dropdown(
                            id='drop_teachers',
                            options=teachers_dict,
                            value=teachers_list[0]
                        ),
                        md=8
                    )
                    
                ]), 
                dbc.Row([
                    dbc.Col(dbc.Label("Curso"), md=4),
                    dbc.Col(
                        dcc.Dropdown(
                            id='drop_class',
                            options=classes_dict,
                            value=classes_id[0]
                        ),
                        md=8
                    )
                    
                ]),
            ]),
        ]),
        fluid=True
    ),
    html.Div(
        dbc.Container(
            dcc.Checklist(
            id='check_students',
            #options=class1A_dict,
            style={"display":"block"},
            labelStyle={'display': 'block'},
            inputStyle={"margin-right": "20px"}
            ),
        ),
        id='div_to_hide',
        style= {'display': 'block'}
        
    ),
    html.Div(
    #dbc.Container(
        dbc.Container(
            dbc.Col(dcc.Graph(id="graph"), width=12),
            fluid=True
        ),
        id='div_to_show',
        style= {'display': 'none'}
        
    ),
    dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col(md=9),
                dbc.Col(
                    dbc.Button(
                        "Guardar",
                        id='button_save',
                        color="primary"),
                    md=3
                ),
                # dbc.Col(
                #     dbc.Button(
                #         "Show",
                #         id='button_graph',
                #         disabled = True,
                #         color="primary"),
                #     md=3                        
                # ),
                # dbc.Col(md=3)
            ])
                
        )
            
    )
 ])

# https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
# @app.callback(
#     Output(component_id='div_to_hide', component_property='style'),
#     Output(component_id='div_to_show', component_property='style'),
#     [Input(component_id='button_save', component_property='n_clicks')])

# def show_hide_element(trigger):
#     if trigger:
#         return {'display': 'none'}, {'display': 'block'}
#     else:
#         return {'display': 'block'}, {'display': 'none'}




# Callback to update list of students
@app.callback(
    Output(component_id='check_students', component_property='options'),
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
    
    return class_dict

@app.callback(
    #Output("button_graph", "disabled"),
    Output(component_id='check_students', component_property='value'),
    Output(component_id='div_to_hide', component_property='style'),
    Output(component_id='div_to_show', component_property='style'),
    Output(component_id='graph', component_property='figure'),
    [Input("button_save", "n_clicks")],    
    [Input('drop_class', 'value')],
    [Input('date-picker', 'date')],
    [Input('drop_teachers', 'value')],
    [State("check_students", "value")], 
)
def save_in_googlesheets(trigger, 
                         selec_class, 
                         date_picked, 
                         teacher_name, 
                         values):
    if trigger:
        if values == None:
            values = []
        book_class_id = classes_list[selec_class]
        book_class = gc.open_by_key(book_class_id)
        worksheet = book_class.worksheet('Estudiantes')
        #url_class = f"https://docs.google.com/spreadsheets/d/{book_class}/gviz/tq?tqx=out:csv&sheet={'Estudiantes'}"
        #df_class= pd.read_csv(url_class)
        df_class = pd.DataFrame(worksheet.get_all_records())
        df = df_class[df_class['nombre'].isin(values)]
        df.insert(0, 'fecha', date_picked)
        df['curso'] = selec_class
        df['prof_reporta'] = teacher_name 
        df_values = df.values.tolist()
        # save in class id
        book_class = gc.open_by_key(book_class_id)
        book_class.values_append('Faltas', {'valueInputOption': 'RAW'}, {'values': df_values})
        # save in consolidate sheet
        book_consolidate = gc.open_by_key(book_consolidate_id)
        book_consolidate.values_append('Consolidado', {'valueInputOption': 'RAW'}, {'values': df_values})
        #return False, list()
        # Create graph
        
        worksheet = book_consolidate.worksheet('Consolidado')
        df_asistencia = pd.DataFrame(worksheet.get_all_records())
        df_cum = df_asistencia.groupby("fecha").codigo.agg(conteo=('count'))
        df_cum.reset_index(inplace=True)
        df_cum = df_cum.sort_values(by=['fecha'])
       
        fig = px.line(df_cum, x="fecha", y="conteo", title='Precio promedio de la habichuela en Medelín')

        return list(), {'display': 'none'}, {'display': 'block'}, fig
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
    


