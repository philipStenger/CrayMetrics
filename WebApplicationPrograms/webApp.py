# Program that creates a Dash Plotly interactive web application for crayfish data analytics
import sqlite3
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import timedelta, datetime
import pandas as pd
import numpy as np

def get_heatmap_data(option, lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date):
    # Connect to the database
    connection = sqlite3.connect("DatabasePrograms\crayfish_catch.db")

    end_date_str = end_date.split("T")[0] # Extract only the date part
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)

    start_date_str = start_date.split("T")[0] # Extract only the date part
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        # Depending on the interval, adjust the SQL query to group by that interval
    if interval == 'hour':
        time_grouping = "strftime('%Y-%m-%d %H:00:00', time)"
    elif interval == 'month':
        time_grouping = "strftime('%Y-%m', time)"
    else: # default to day
        time_grouping = "strftime('%Y-%m-%d', time)"

    # Create a filter for latitude and longitude
    lat_lon_filter = f'WHERE c.latitude BETWEEN {lat_min} AND {lat_max} AND c.longitude BETWEEN {lon_min} AND {lon_max}'
    date_filter = f"AND time >= '{start_date}' AND time <= '{end_date}'"
    print("option: ", option)

    if option == 'Weight':
        query = f'''
            SELECT {time_grouping} as time_interval, c.latitude, c.longitude, SUM(c.weight) as value
            FROM catches AS c
            JOIN batches AS b ON c.batch_id = b.batch_id
            {lat_lon_filter} {date_filter}
            GROUP BY time_interval, c.latitude, c.longitude
        '''
    else:  # Number of Catches
        query = f'''
            SELECT {time_grouping} as time_interval, c.latitude, c.longitude, COUNT(c.catch_id) as value
            FROM catches AS c
            {lat_lon_filter} {date_filter}
            GROUP BY time_interval, c.latitude, c.longitude
        '''

    print("query: ", query)

    # Execute query and read the result into a DataFrame
    df = pd.read_sql_query(query, connection)

    print(df.head())

    # Close the connection
    connection.close()

    return df

def get_time_series_data(lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date):
    connection = sqlite3.connect('DatabasePrograms\crayfish_catch.db')

    end_date_str = end_date.split("T")[0] # Extract only the date part
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)

    start_date_str = start_date.split("T")[0] # Extract only the date part
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    # Depending on the interval, adjust the SQL query to group by that interval
    if interval == 'hour':
        time_grouping = "strftime('%Y-%m-%d %H:00:00', time)"
    elif interval == 'month':
        time_grouping = "strftime('%Y-%m', time)"
    else: # default to day
        time_grouping = "strftime('%Y-%m-%d', time)"

    date_filter = f"AND time >= '{start_date}' AND time <= '{end_date}'"

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
          {date_filter}
        GROUP BY {time_grouping}
        ORDER BY {time_grouping}
    '''

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df

def create_heatmap(option, lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date):
    df = get_heatmap_data(option, lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date)

    if option == 'Weight':
        max_catch_count = 80
    else:
        max_catch_count = 1

    fig = px.density_mapbox(df, 
                            lat='latitude', 
                            lon='longitude', 
                            z='value', 
                            radius=8,
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
        
        title_text=f"{option} by Location",
        mapbox_style="stamen-terrain",
        width=600,  # Width of the figure in pixels
        height=600,  # Height of the figure in pixels
        showlegend=False,
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
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
        title='Crayfish Catch Metrics by Time Interval',
        yaxis=dict(title='Total Weight / Number of Catches'),
        yaxis2=dict(title='Average Weight'),
        xaxis=dict(title='Time Interval')
    )

    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    # Title
    html.Div([
        html.H2("CrayMetrics Data Analytics Platform", style={'textAlign': 'center'}),
    ], style={'margin-bottom': '20px'}),
    
    # Configuration
    html.Div([
        # Time Configuration
        html.Div([
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
                        min_date_allowed=pd.Timestamp('2023-01-01'),
                        max_date_allowed=pd.Timestamp('today'),
                        date=datetime(2023, 1, 1),
                    ),
                ], style={'width': '20%', 'display': 'inline-block'}),
                html.Div([
                    html.Label('End Date: '),
                    dcc.DatePickerSingle(
                        id='end-date',
                        min_date_allowed=pd.Timestamp('2023-01-01'),
                        max_date_allowed=pd.Timestamp('today'),
                        date=datetime.today(),
                    ),
                ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'margin-bottom': '20px'}),
        ], style={'padding': '15px', 'border-bottom': '1px solid #ccc'}),
        
        # Data Options and Toggle Lines
        html.Div([
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
        ], style={'padding': '15px', 'border-bottom': '1px solid #ccc'}),
        
        # Coordinate Ranges
        html.Div([
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
        ], style={'padding': '15px'}),
    ], style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ccc', 'background-color': '#f9f9f9'}),

    # Heatmap and Time Series
    html.Div([
        html.Div([
            dcc.Graph(id='heatmap'),
        ], style={'display': 'inline-block', 'width': '49%', 'padding': '5px'}),
        html.Div([
            dcc.Graph(id='time-series'),
        ], style={'display': 'inline-block', 'width': '49%', 'padding': '5px'}),
    ], style={'margin': '10px'}),
])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('toggle-menu', 'value'),
     Input('lat_min', 'value'),
     Input('lat_max', 'value'),
     Input('lon_min', 'value'),
     Input('lon_max', 'value'),
     Input('time-interval', 'value'),
     Input('start-date', 'date'),  # Add this line
     Input('end-date', 'date')]  # Add this line
)
def update_heatmap(selected_value, lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date):
    return create_heatmap(selected_value, lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date)

@app.callback(
    Output('time-series', 'figure'),
    [Input('lat_min', 'value'),
     Input('lat_max', 'value'),
     Input('lon_min', 'value'),
     Input('lon_max', 'value'),
     Input('time-interval', 'value'),
     Input('line-toggle', 'value'),
     Input('start-date', 'date'),  # Add this line
     Input('end-date', 'date')]  # Add this line
)
def update_time_series(lat_min, lat_max, lon_min, lon_max, interval, line_toggle, start_date, end_date):
    df = get_time_series_data(lat_min, lat_max, lon_min, lon_max, interval, start_date, end_date)
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
        title=f'Crayfish Catch Metrics by {interval.capitalize()}',
        yaxis=dict(title='Total Weight / Number of Catches'),
        yaxis2=dict(title='Average Weight'),
        xaxis=dict(title='Time Interval')
    )

    return fig

if __name__ == '__main__':

    app.run_server(debug=True)

