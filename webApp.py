# Program that creates a Dash Plotly interactive web application for crayfish data analytics
import sqlite3
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import numpy as np

def get_heatmap_data(option, lat_min, lat_max, lon_min, lon_max):
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')

    if lat_min is None:
        lat_min = -43  # default value, or raise an exception if this is an error
    
    if lat_max is None:
        lat_max = -15  # default value, or raise an exception if this is an error

    if lon_min is None:
        lon_min = 150  # default value, or raise an exception if this is an error

    if lon_max is None:
        lon_max = 200  # default value, or raise an exception if this is an error

    # Add WHERE clause to filter data based on latitude and longitude ranges
    lat_lon_filter = f'''
        WHERE c.latitude BETWEEN {lat_min} AND {lat_max}
        AND c.longitude BETWEEN {lon_min} AND {lon_max}
    '''

    if option == 'Weight':
        query = f'''
            SELECT c.latitude, c.longitude, c.weight
            FROM catches AS c
            JOIN batches AS b ON c.batch_id = b.batch_id
            {lat_lon_filter}
        '''
    else:  # Number of Catches
        query = f'''
            SELECT c.latitude, c.longitude, COUNT(c.catch_id) as catch_count
            FROM catches AS c
            {lat_lon_filter}
            GROUP BY c.batch_id, c.latitude, c.longitude
        '''

    # Execute query and read the result into a DataFrame
    df = pd.read_sql_query(query, connection)

    # Close the connection
    connection.close()

    return df

def get_time_series_data(lat_min, lat_max, lon_min, lon_max, interval='day'):
    connection = sqlite3.connect('crayfish_catch.db')

    # Depending on the interval, adjust the SQL query to group by that interval
    if interval == 'hour':
        time_grouping = "strftime('%Y-%m-%d %H:00:00', time)"
    elif interval == 'week':
        time_grouping = "strftime('%Y-%W', time)"
    else: # default to day
        time_grouping = "strftime('%Y-%m-%d', time)"

    query = f'''
        SELECT {time_grouping} as time_interval,
               SUM(c.weight) as total_weight,
               CASE
                   WHEN COUNT(c.catch_id) > 0 THEN SUM(c.weight) / COUNT(c.catch_id)
                   ELSE 0
               END as avg_weight,
               COUNT(c.catch_id) as num_catches
        FROM catches AS c
        WHERE c.latitude BETWEEN {lat_min} AND {lat_max}
          AND c.longitude BETWEEN {lon_min} AND {lon_max}
        GROUP BY {time_grouping}
        ORDER BY {time_grouping}
    '''

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df

def create_heatmap(option, lat_min, lat_max, lon_min, lon_max):
    
    df = get_heatmap_data(option, lat_min, lat_max, lon_min, lon_max)
    if option == 'Weight':
        z_value = 'weight'
        max_catch_count = 50
    else:
        z_value = 'catch_count'
        max_catch_count = 6

    fig = px.density_mapbox(df, 
                            lat='latitude', 
                            lon='longitude', 
                            z=z_value, 
                            radius=10,
                            center=dict(lat= -40, lon= 175), 
                            zoom=3,
                            mapbox_style="stamen-terrain", 
                            range_color=(1, max_catch_count))

    # Set the bounds of the map to cover only the specific area of interest
    fig.update_geos(
        projection_type="mercator",
        lonaxis=dict(range=[lon_min, lon_max]),
        lataxis=dict(range=[lat_min, lat_max])
    )

        # Set the size of the figure to be square
    fig.update_layout(
        mapbox_style="stamen-terrain",
        width=800,  # Width of the figure in pixels
        height=800,  # Height of the figure in pixels
        showlegend=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

        # Add latitude and longitude grid lines (you can modify the step)
    lat_lines = np.arange(lat_min, lat_max, step=5)  # Adjust step as needed
    lon_lines = np.arange(lon_min, lon_max, step=5)  # Adjust step as needed

    for lat in lat_lines:
        fig.add_scattermapbox(lat=[lat, lat], lon=[lon_min, lon_max], mode="lines", line=dict(width=1, color="gray"))

    for lon in lon_lines:
        fig.add_scattermapbox(lat=[lat_min, lat_max], lon=[lon, lon], mode="lines", line=dict(width=1, color="gray"))


    return fig

def create_time_series_plot(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['time_interval'], y=df['total_weight'], name='Total Weight', mode='lines'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=df['time_interval'], y=df['num_catches'], name='Number of Catches', mode='lines'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=df['time_interval'], y=df['avg_weight'], name='Average Weight', mode='lines'),
        secondary_y=True
    )

    fig.update_layout(
        title='Crayfish Catch Metrics Over Time',
        yaxis=dict(title='Total Weight / Number of Catches'),
        yaxis2=dict(title='Average Weight'),
        xaxis=dict(title='Time Interval')
    )

    return fig




app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.RadioItems(
        id='toggle-menu',
        options=[{'label': 'Weight', 'value': 'Weight'},
                 {'label': 'Number of Catches', 'value': 'Number of Catches'}],
        value='Weight',
        labelStyle={'display': 'inline-block'}
    ),
    html.Div([
        html.Label('Latitude Range:'),
        dcc.Input(id='lat_min', type='number', value=-53),
        dcc.Input(id='lat_max', type='number', value=-15),
    ]),
    html.Div([
        html.Label('Longitude Range:'),
        dcc.Input(id='lon_min', type='number', value=150),
        dcc.Input(id='lon_max', type='number', value=200),
    ]),
    dcc.Graph(id='heatmap'),
    html.Div([
        html.Label('Select Time Interval:', style={'display': 'block'}),
        dcc.Dropdown(
            id='time-interval',
            options=[{'label': 'Hourly', 'value': 'hour'},
                     {'label': 'Daily', 'value': 'day'},
                     {'label': 'Weekly', 'value': 'week'}],
            value='day',
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='time-series', style={'width': '95%'}), # Specify width here
            ], style={'display': 'inline-block', 'width': '95%'}), # And here
            html.Div([
                html.Label('Toggle lines:'),
                dcc.Checklist(
                    id='line-toggle',
                    options=[{'label': 'Total Weight', 'value': 'total_weight'},
                             {'label': 'Number of Catches', 'value': 'num_catches'},
                             {'label': 'Average Weight', 'value': 'avg_weight'}],
                    value=['total_weight', 'num_catches', 'avg_weight'],  # all lines are displayed by default
                ),
            ], style={'display': 'inline-block', 'width': '15%', 'height': '50px', 'vertical-align': 'top', 'padding-left': '5px', 'padding-top': '5px'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),
    ])
])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('toggle-menu', 'value'),
     Input('lat_min', 'value'),
     Input('lat_max', 'value'),
     Input('lon_min', 'value'),
     Input('lon_max', 'value')]
)
def update_heatmap(selected_value, lat_min, lat_max, lon_min, lon_max):
    return create_heatmap(selected_value, lat_min, lat_max, lon_min, lon_max)

@app.callback(
    Output('time-series', 'figure'),
    [Input('lat_min', 'value'),
     Input('lat_max', 'value'),
     Input('lon_min', 'value'),
     Input('lon_max', 'value'),
     Input('time-interval', 'value'),
     Input('line-toggle', 'value')]  # Add this line to get the checkbox values
)
def update_time_series(lat_min, lat_max, lon_min, lon_max, interval, line_toggle):
    df = get_time_series_data(lat_min, lat_max, lon_min, lon_max, interval)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if 'total_weight' in line_toggle:
        fig.add_trace(
            go.Scatter(x=df['time_interval'], y=df['total_weight'], name='Total Weight', mode='lines'),
            secondary_y=False
        )
    if 'num_catches' in line_toggle:
        fig.add_trace(
            go.Scatter(x=df['time_interval'], y=df['num_catches'], name='Number of Catches', mode='lines'),
            secondary_y=False
        )
    if 'avg_weight' in line_toggle:
        fig.add_trace(
            go.Scatter(x=df['time_interval'], y=df['avg_weight'], name='Average Weight', mode='lines'),
            secondary_y=True
        )

    fig.update_layout(
        title='Crayfish Catch Metrics Over Time',
        yaxis=dict(title='Total Weight / Number of Catches'),
        yaxis2=dict(title='Average Weight'),
        xaxis=dict(title='Time Interval')
    )

    return fig


if __name__ == '__main__':

    app.run_server(debug=True)

