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

# Para que funcionen los Dropdowns y otros items de lista
available_hours = df['Hour'].unique()
weekdays = [
    {'label': 'Monday', 'value': 0},
    {'label': 'Tuesday', 'value': 1},
    {'label': 'Wednesday', 'value': 2},
    {'label': 'Thursday', 'value': 3},
    {'label': 'Friday', 'value': 4},
    {'label': 'Saturday', 'value': 5},
    {'label': 'Sunday', 'value': 6}
]
months = [
    {'label': 'January', 'value': 1},
    {'label': 'February', 'value': 2},
    {'label': 'March', 'value': 3},
    {'label': 'April', 'value': 4},
    {'label': 'May', 'value': 5},
    {'label': 'June', 'value': 6},
    {'label': 'July', 'value': 7},
    {'label': 'August', 'value': 8},
    {'label': 'September', 'value': 9},
    {'label': 'October', 'value': 10},
    {'label': 'November', 'value': 11},
    {'label': 'December', 'value': 12}
]

Yes_No = [
    {'label': 'Yes', 'value': 1},
    {'label': 'No', 'value': 0},
]

#Layout App
app.layout = html.Div([
    html.H1("- RENTAL BIKES DASHBOARD -", style={'fontFamily': 'Courier New' ,'color': 'green','textAlign': 'center', 'backgroundColor': '#ebf7e8'}),
    html.Img(src='https://raw.githubusercontent.com/lbtriana/Proyecto_Bicicletas/main/Anexos_dash/20210708000693_0.jpg',
        style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '20%'}),
    html.Div([
        #COLUMNA 1 - COLUMNA IZQUIERDA - ANALISIS POR HORA
        html.Div([
            #SECCIÓN PREDICCION DEMANDA - HORA
            html.H3('DEMAND PREDICTION PER HOUR:', 
                    style={'fontFamily': 'Courier New' ,'color': 'green','textAlign': 'center', 'backgroundColor': '#ebf7e8'}),
            html.H5('Please enter the values to predict demand:', 
                    style={'fontFamily': 'Helvetica' ,'color': '#585858','textAlign': 'left'}),
            html.H6('(make sure the input makes sense, for example that the month and is_winter make sense)', 
                    style={'fontFamily': 'Helvetica' ,'color': '#7f807f','textAlign': 'left'}),
            html.H6('(make sure input makes sense, for example that the month and is_winter dont contradict each other)', 
                    style={'fontFamily': 'Helvetica' ,'color': '#7f807f','textAlign': 'left'}),
            html.Div([
                #HORA
                html.Div([
                    html.H6('Hour', style={'textAlign':'center'}),
                    dcc.Dropdown(
                        id='hour-dropdown', 
                        options=[{'label': i, 'value': i} for i in available_hours],
                        value=12)
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #WEEKDAY
                html.Div([
                    html.H6('Weekday', style={'textAlign':'center'}),
                    dcc.Dropdown(
                        id='weekdays_h-dropdown', 
                        options=weekdays,
                        value=3),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #MONTH
                html.Div([
                    html.H6('Month', style={'textAlign':'center'}),
                    dcc.Dropdown(
                        id='month_h-dropdown', 
                        options=months,
                        value=7),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #TEMPERATURE
                html.Div([
                    html.H6('Temperature', style={'textAlign':'center'}),
                    dcc.Input(
                        id='temperature_h-input',
                        type='number',
                        min= df['Temperature(C)'].min(),
                        max= df['Temperature(C)'].max(),
                        step=0.1,
                        value= round(df['Temperature(C)'].mean(), 1)),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #HUMIDITY
                html.Div([
                    html.H6('Humidity %', style={'textAlign':'center'}),
                    dcc.Input(
                        id='humidity_h-input',
                        type='number',
                        min= df['Humidity(%)'].min(),
                        max= df['Humidity(%)'].max(),
                        step=1,
                        value= round(df['Humidity(%)'].mean(),0)),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #RAINFALL MM
                html.Div([
                    html.H6('Rainfall (mm)', style={'textAlign':'center'}),
                    dcc.Input(
                        id='rainfall_h-input',
                        type='number',
                        min= df['Rainfall(mm)'].min(),
                        max= df['Rainfall(mm)'].max(),
                        step=0.1,
                        value= round(df['Rainfall(mm)'].mean(),1)),
                ], style={'display': 'inline-block', 'padding': '30px'}),

            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
            
            html.Div([
                #HOLIDAY
                html.Div([
                    html.H6('Holiday?', style={'textAlign':'center'}),
                    dcc.RadioItems(
                        id='holiday_h-radio',
                        options=Yes_No,
                        value=0),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #WINTER
                html.Div([
                    html.H6('Winter?', style={'textAlign':'center'}),
                    dcc.RadioItems(
                        id='winter_h-radio',
                        options=Yes_No,
                        value=0),
                ], style={'display': 'inline-block', 'padding': '30px'}),

            ], style={'display': 'inline-block', 'padding': '30px'}),
 
        ],style={'width': '48%', 'float': 'left', 'display': 'inline-block'}), #, 'backgroundColor': '#fcfcfc'

        #COLUMNA 2 - COLUMNA DERECHA - ANALISIS POR DIA
        html.Div([
            #SECCIÓN PREDICCION DEMANDA - DIA
            html.H3('DEMAND PREDICTION PER DAY:', 
                    style={'fontFamily': 'Courier New' ,'color': 'green','textAlign': 'center', 'backgroundColor': '#ebf7e8'}),
            html.H5('Please enter the values to predict demand:', 
                    style={'fontFamily': 'Helvetica' ,'color': '#585858','textAlign': 'left'}),
            html.H6('(make sure the input makes sense, for example that the month and is_winter make sense)', 
                    style={'fontFamily': 'Helvetica' ,'color': '#7f807f','textAlign': 'left'}),
            html.H6('(make sure input makes sense, for example that the month and is_winter dont contradict each other)', 
                    style={'fontFamily': 'Helvetica' ,'color': '#7f807f','textAlign': 'left'}),
            html.Div([
                #WEEKDAY
                html.Div([
                    html.H6('Weekday', style={'textAlign':'center'}),
                    dcc.Dropdown(
                        id='weekdays_d-dropdown', 
                        options=weekdays,
                        value=3),
                ], style={'display': 'inline-block', 'padding': '30px'}),

                #MONTH
                html.Div([
                    html.H6('Month', style={'textAlign':'center'}),
                    dcc.Dropdown(
                        id='month_d-dropdown', 
                        options=months,
                        value=7),
                ], style={'display': 'inline-block', 'padding': '30px'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
            dcc.Dropdown(),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ])
])

# Para correr la app
if __name__ == '__main__':
    app.run_server(debug=True)