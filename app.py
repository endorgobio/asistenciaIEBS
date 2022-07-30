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
#url_acopios = f"https://docs.google.com/spreadsheets/d/{book_id}/gviz/tq?tqx=out:csv&sheet={sheet_acopios}"
df_teachers= pd.read_csv(url_teachers)
df_lists= pd.read_csv(url_lists)
#df_acopios = pd.read_csv(url_acopios)

