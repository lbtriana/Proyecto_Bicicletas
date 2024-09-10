import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context # Para que la URL del archivo cvs funcione en mac

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

ruta = "https://raw.githubusercontent.com/lbtriana/Proyecto_Bicicletas/main/SeoulBikeData_utf8.csv" #ruta desde url
df = pd.read_csv(ruta)

app.layout = html.Div([
    html.H1("Rental Bikes Dashboard", style={'textAlign': 'center'}),
    html.Img( src='Anexos_dash/20210708000693_0.jpg',
        style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'}),
    html.Div([

        html.Div([
            dcc.Dropdown(
                
            ),
            dcc.RadioItems(
                
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                
            ),
            dcc.RadioItems(
                
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
])
# Para correr la app
if __name__ == '__main__':
    app.run_server(debug=True)