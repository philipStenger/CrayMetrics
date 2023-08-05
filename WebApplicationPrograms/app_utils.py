from dash import dcc
from dash import html
from datetime import datetime
import pandas as pd

def create_title():
    return html.Div([
        html.H2("CrayMetrics Data Analytics Platform", style={'textAlign': 'center'}),
    ], style={'margin-bottom': '20px'})

def create_time_configuration():
    return html.Div([
        html.Label('Time Configuration', style={'font-weight': 'bold', 'font-size': '18px'}),
        html.Div([
            html.Div([
                html.Label('Interval:'),
                dcc.Dropdown(
                    id='time-interval',
                    options=[{'label': 'Hourly', 'value': 'hour'},
                            {'label': 'Daily', 'value': 'day'},
                            {'label': 'Monthly', 'value': 'month'}],
                    value='day',
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'padding-right': '20px'}),
            html.Div([
                html.Label('Start Date: '),
                dcc.DatePickerSingle(
                    id='start-date',
                    min_date_allowed=pd.Timestamp('2022-01-01'),
                    max_date_allowed=pd.Timestamp('today'),
                    date=datetime(2022, 1, 1),
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                html.Label('End Date: '),
                dcc.DatePickerSingle(
                    id='end-date',
                    min_date_allowed=pd.Timestamp('2022-01-01'),
                    max_date_allowed=pd.Timestamp('today'),
                    date=datetime(2023, 1, 1),
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),
        ], style={'margin-bottom': '20px'}),
    ], style={'padding': '15px', 'border-bottom': '1px solid #ccc'})

def create_data_options():
    return html.Div([
        html.Label('Data Options', style={'font-weight': 'bold', 'font-size': '18px'}),
        html.Div([
            html.Div([
                dcc.RadioItems(
                    id='toggle-menu',
                    options=[{'label': 'Weight', 'value': 'Weight'},
                            {'label': 'Number of Catches', 'value': 'Number of Catches'}],
                    value='Weight',
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Toggle lines:'),
                dcc.Checklist(
                    id='line-toggle',
                    options=[{'label': 'Total Weight', 'value': 'total_weight'},
                            {'label': 'Number of Catches', 'value': 'num_catches'},
                            {'label': 'Average Weight', 'value': 'avg_weight'}],
                    value=['total_weight', 'num_catches', 'avg_weight'],
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ], style={'margin-bottom': '20px'}),
    ], style={'padding': '15px', 'border-bottom': '1px solid #ccc'})

def create_coordinate_ranges():
    return html.Div([
        html.Label('Coordinate Ranges', style={'font-weight': 'bold', 'font-size': '18px'}),
        html.Div([
            html.Div([
                html.Label('Latitude Range:'),
                dcc.Input(id='lat_min', type='number', value=-53),
                dcc.Input(id='lat_max', type='number', value=-15),
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Longitude Range:'),
                dcc.Input(id='lon_min', type='number', value=150),
                dcc.Input(id='lon_max', type='number', value=200),
            ]),
        ], style={'margin-bottom': '20px'}),
    ], style={'padding': '15px'})

def create_heatmap_and_timeseries():
    return html.Div([
        html.Div([
            dcc.Graph(id='heatmap'),
        ], style={'display': 'inline-block', 'width': '49%', 'padding': '5px'}),
        html.Div([
            dcc.Graph(id='time-series'),
        ], style={'display': 'inline-block', 'width': '49%', 'padding': '5px'}),
    ], style={'margin': '10px'})

def create_configuration():
    return html.Div([
        create_time_configuration(),
        create_data_options(),
        create_coordinate_ranges(),
    ], style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ccc', 'background-color': '#f9f9f9'})
