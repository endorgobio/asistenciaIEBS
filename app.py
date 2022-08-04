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
from dash import no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import gspread
from datetime import date
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('access_key.json', 
                                                    scopes=scopes)

gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# books ids
book_teachers_id = '1bqZ8OnYfpM0A6EoVoM_YRurfNmn2UCTAzPYdkZk2vaM'
book_classes_id = '17DTbRs54Y-7nntaSqaIFEHAcMNa4ven6OxDqWswT3rE'
book_consolidate_id = '1w8h3dzb4dqSGDrj_QThuES7J_aqrAx_nwXgY7qUDSA0'

# Read data about teachers
#book_teachers = gc.open_by_key(book_teachers_id)
#worksheet = book_teachers.worksheet('Docentes')
url_teachers = f"https://docs.google.com/spreadsheets/d/{book_teachers_id}/gviz/tq?tqx=out:csv"
df_teachers= pd.read_csv(url_teachers)
#df_teachers= pd.DataFrame(worksheet.get_all_records())
df_teachers = df_teachers.sort_values(by=['nombre'])
teachers_list = df_teachers["nombre"].values.tolist()
teachers_dict = [{"label": k, "value": k} for k in teachers_list]

# Read data about classes
#book_classes = gc.open_by_key(book_classes_id)
#worksheet = book_classes.worksheet('Cursos')
url_classes = f"https://docs.google.com/spreadsheets/d/{book_classes_id}/gviz/tq?tqx=out:csv"
df_classes= pd.read_csv(url_classes)
#df_classes= pd.DataFrame(worksheet.get_all_records())
classes_id = df_classes["curso"].values.tolist()
classes_list = dict(zip(df_classes.curso, df_classes.google_id))
classes_dict = [{"label": k, "value": k} for k in classes_list.keys()]

# Read consolidate data
url_asistencia = f"https://docs.google.com/spreadsheets/d/{book_consolidate_id}/gviz/tq?tqx=out:csv"
df_asistencia= pd.read_csv(url_asistencia)
#book_consolidate = gc.open_by_key(book_consolidate_id)
#worksheet = book_consolidate.worksheet('Consolidado')
#df_asistencia = pd.DataFrame(worksheet.get_all_records())


# Define stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]


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
                    id='description'
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
                dbc.Col(md=6),
                dbc.Col(
                    dbc.Button(
                        "Guardar",
                        id='button_save',
                        color="primary"),
                    md=3
                ),
                dbc.Col([
                    dbc.Button(
                        "Ver datos",
                        id='download',
                        disabled = True,
                        color="primary"),
                    # Store inside the app joined dataframe
                    dcc.Store(id='consolidate_data'),   
                    # Download stored data
                    dcc.Download(id="download-dataframe-csv")],
                    md=3                        
                ),
                #dbc.Col(md=3)
            ])
                
        )
            
    ),

 ])



# Callback to update list of students
@app.callback(
    Output(component_id='check_students', component_property='options'),
    Input(component_id='drop_class', component_property='value')
    )
def update_list(selec_class):
    book_class_id = classes_list[selec_class]
    sheet_estudiantes = 'Estudiantes'
    book_class = gc.open_by_key(book_class_id)
    worksheet = book_class.worksheet('Estudiantes')
    df_class = pd.DataFrame(worksheet.get_all_records())  
    df_class = df_class.sort_values(by=['nombre'])
    class_list = list(zip(df_class.codigo, df_class.nombre))
    class_dict = [{"label": k[1], "value": k[1]} for k in class_list]
    
    return class_dict

@app.callback(
    Output("button_save", "disabled"),
    Output("download", "disabled"),
    Output('check_students', 'value'),
    Output('div_to_hide', 'style'),
    Output('div_to_show', 'style'),
    Output('graph', 'figure'),
    Output('consolidate_data', 'data'),
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
        
        # Open workbook of the class
        book_class_id = classes_list[selec_class]
        book_class = gc.open_by_key(book_class_id)
        worksheet = book_class.worksheet('Estudiantes')
        df_class = pd.DataFrame(worksheet.get_all_records())
        df = df_class[df_class['nombre'].isin(values)]
        df.insert(0, 'fecha', date_picked)
        df['curso'] = selec_class
        df['prof_reporta'] = teacher_name 
        df_values = df.values.tolist()
        # save in class id
        book_class = gc.open_by_key(book_class_id)
        book_class.values_append('Faltas', 
                                 {'valueInputOption': 'RAW'}, 
                                 {'values': df_values})
        # save in consolidate sheet
        book_consolidate = gc.open_by_key(book_consolidate_id)
        book_consolidate.values_append('Consolidado', 
                                       {'valueInputOption': 'RAW'}, 
                                       {'values': df_values})
        
        
        df_joined = pd.concat([df_asistencia, df])
        data_consolidated = df_joined.to_json(date_format='iso', orient='split')
        
        
        df_cum = df_joined.groupby("fecha").codigo.agg(conteo=('count'))
        df_cum.reset_index(inplace=True)
        df_cum = df_cum.sort_values(by=['fecha'])
        
        fig = px.line(df_cum, x="fecha", y="conteo", 
                      title='Historico de Ausentismo')
        fig.update_layout(title_x=0.5)
        return True, False, list(), {'display': 'none'}, {'display': 'block'}, \
            fig, data_consolidated
    else:
        return dash.no_update


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download", "n_clicks"),
    Input('consolidate_data', 'data'),
    prevent_initial_call=True,
)
def func(trigger, jsonified_data):
    if trigger:
        #df_asistencia = pd.read_json(jsonified_data, orient='split')
        url_asistencia = f"https://docs.google.com/spreadsheets/d/{book_consolidate_id}/gviz/tq?tqx=out:csv"
        df_asistencia= pd.read_csv(url_asistencia)
        return dcc.send_data_frame(df_asistencia.to_csv, "asistencia.csv")
    else:
        return dash.no_update


# app.clientside_callback(
#     """
#     function(trigger) {
#         if trigger > 0:
#             link = 'https://docs.google.com/spreadsheets/d/1w8h3dzb4dqSGDrj_QThuES7J_aqrAx_nwXgY7qUDSA0/edit?usp=sharing'
#             window.open(link)
#             return white_button_style
#         else:
#             return white_button_style
#     }
#     """,
#     Output('download', 'style'),
#     Input("download", "n_clicks"),
#     prevent_initial_call=True,
# )



if __name__ == "__main__":
    app.run_server(debug=True)
    


