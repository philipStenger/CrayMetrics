import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from db_utils import get_heatmap_data

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

