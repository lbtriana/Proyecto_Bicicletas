import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import seaborn as sns
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

# Modificar variables
df['fecha'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['month'] = df['fecha'].dt.month
df['year'] = df['fecha'].dt.year
df['day_of_week'] = df['fecha'].dt.dayofweek
df['Hour_PM'] = np.where(df['Hour'] >= 12, 1, 0) #1 si es hora en la tarde 
df['Hour_lab'] = np.where((df['Hour'] >= 8) & (df['Hour'] <= 17), 1, 0) #1 si es horario laboral


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

available_var_graph = df.columns.tolist()

variables_box_plot = ['Hour', 'month', 'year','day_of_week', 'Holiday', 'Hour_PM', 'Hour_lab', 'Seasons', 'Functioning Day']

#Layout App
app.layout = html.Div([
    html.H1("- RENTAL BIKES DASHBOARD -", style={'fontFamily': 'Courier New' ,'color': 'green','textAlign': 'center', 'backgroundColor': '#ebf7e8'}),
    html.Img(src='https://raw.githubusercontent.com/lbtriana/Proyecto_Bicicletas/main/Anexos_dash/20210708000693_0.jpg',
        style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '20%'}),
    html.Div([
        html.H3('- GRAPH CREATOR -', style={'fontFamily': 'Courier New' ,'color': '#55aaab','textAlign': 'center', 'backgroundColor': '#dff5f5'}),
        html.H6('This section leverages historical data from the Rental Bike business for the years 2016 and 2017. It allows the user to generate boxplots or scatter graphs to visualize the relationship between the Rented Bike Count (Y-axis) and the independent variables (X-axis). The goal is to provide insights into the hourly patterns and trends in bike rentals, enabling a deeper analysis of how different factors influence rental behavior.', 
                    style={'fontFamily': 'Helvetica' ,'color': '#7f807f','textAlign': 'left'}),
        html.Br(),
    ], style={'margin-right': '500px', 'margin-left': '500px'}),
    html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in available_var_graph], # PENDIENTE REVISAR
            value='Seasons'
            ),
        dcc.Graph(id='fig_graph_creator'),
    ], style={'margin-right': '400px', 'margin-left': '400px', 'height': 'auto'}),
    html.Div([
        #COLUMNA 1 - COLUMNA IZQUIERDA - ANALISIS PREDICCION DEMANDA POR HORA
        html.Div([
            
            html.H3('- DEMAND PREDICTION PER HOUR -', 
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

            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
            
            html.Div([
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

            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

            html.Div([
                html.Div([
                    html.H4('PREDICTED DEMAND PER HOUR', style={'color': 'orange', 'fontFamily': 'Courier New','textAlign':'center'}),
                    html.Div(id='output-Demand-h', style={'color': 'orange', 'fontSize': 20, 'fontFamily': 'Courier New', 'textAlign':'center', 'marginTop': 20}), #revisar si funciona
                    html.H6('Confidence Interval', style={'color': 'orange', 'fontFamily': 'Helvetica','textAlign':'center', 'fontSize': 10}),
                    html.Div(id='output-CInverval-Demand-h', style={'color': 'orange', 'fontFamily': 'Helvetica', 'textAlign':'center', 'fontSize': 12}) # traerlo con corchetes
                ], style={'backgroundColor': '#fef0e2', 'margin-right': '200px', 'margin-left': '200px'}),
                ]
            ),
            html.Br(),
            
 
        ],style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),

        #COLUMNA 2 - COLUMNA DERECHA - INCOME AND COST CALCULATOR
        html.Div([
            
            html.H3('- INCOME AND COST CALCULATOR -', 
                    style={'fontFamily': 'Courier New' ,'color': '#4dc2a9','textAlign': 'center', 'backgroundColor': '#d7fef6'}),
            html.H5('Please enter values:', 
                    style={'fontFamily': 'Helvetica' ,'color': '#585858','textAlign': 'left'}),
            html.Div([
                #HOUR RENTAL PRICE
                    html.Div([
                        html.H6('Hour Rental Price', style={'textAlign':'center'}),
                        dcc.Input(
                            id='hour_rental_price-input',
                            type='number',
                            min= 0,
                            step=0.01,
                            value= 1.25),
                    ], style={'display': 'inline-block', 'padding': '30px'}),

                    #Variable cost per rented hour
                    html.Div([
                        html.H6('Variable cost per rented hour', style={'textAlign':'center'}),
                        dcc.Input(
                            id='cost_per_rented_h-input',
                            type='number',
                            min= 0,
                            step=0.01,
                            value= 0.70),
                    ], style={'display': 'inline-block', 'padding': '30px'}),

                    #Fixed costs per hour
                    html.Div([
                        html.H6('Fixed costs per hour', style={'textAlign':'center'}),
                        dcc.Input(
                            id='fixed_costs_h-input',
                            type='number',
                            min= 0,
                            step=0.01,
                            value= 1000),
                    ], style={'display': 'inline-block', 'padding': '30px'}),
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
            html.Div([
                html.Div([
                    html.H4('TOTAL INCOME PER HOUR', style={'color': 'orange', 'fontFamily': 'Courier New','textAlign':'center'}),
                    html.Div(id='output_total_income-h', style={'color': 'orange', 'fontSize': 20, 'fontFamily': 'Courier New', 'textAlign':'center', 'marginTop': 20}),
                ], style={'backgroundColor': '#fef0e2', 'margin-right': '200px', 'margin-left': '200px'}),
                html.Br(),
                html.Div([
                    html.H4('TOTAL COSTS PER HOUR', style={'color': 'orange', 'fontFamily': 'Courier New','textAlign':'center'}),
                    html.Div(id='output_total_costs-h', style={'color': 'orange', 'fontSize': 20, 'fontFamily': 'Courier New', 'textAlign':'center', 'marginTop': 20}),
                ], style={'backgroundColor': '#fef0e2', 'margin-right': '200px', 'margin-left': '200px'}),
                html.Br(),
                html.Div([
                    html.H4('PROFIT MARGIN PER HOUR', style={'color': 'orange', 'fontFamily': 'Courier New','textAlign':'center'}),
                    html.Div(id='output_profit_margin-h', style={'color': 'orange', 'fontSize': 20, 'fontFamily': 'Courier New', 'textAlign':'center', 'marginTop': 20}),
                ], style={'backgroundColor': '#fef0e2', 'margin-right': '200px', 'margin-left': '200px'}),
                ]
            ),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ])
])

#CALLBACK Y FUNCION PARA ACTUALIZAR GRAFICA - GRAPH CREATOR
@app.callback(
    Output('fig_graph_creator', 'figure'),
    Input('xaxis-column', 'value'),
)
def update_graph(xaxis_column_name):
    if xaxis_column_name in variables_box_plot:
        fig = px.box(df, x=xaxis_column_name, y="Rented Bike Count", title="Boxplot of Values by Category")
    else:
        fig = px.scatter(df, x=xaxis_column_name, y="Rented Bike Count", title="Boxplot of Values by Category")

    return fig


#CALLBACK CALCULADORA INCOME & COST
#@app.callback(
#    [Output('output_total_income-h', 'value'),
#     Output('output_total_costs-h', 'value'),
#     Output()]
#)

# Para correr la app
if __name__ == '__main__':
    app.run_server(debug=True)