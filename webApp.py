# Program that creates a Dash Plotly interactive web application for crayfish data analytics
import sqlite3
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

def get_heatmap_data(option):
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')

    # SQL query to retrieve data from catches and join with batches
    if option == 'Weight':
        query = '''
            SELECT c.latitude, c.longitude, c.weight
            FROM catches AS c
            JOIN batches AS b ON c.batch_id = b.batch_id
        '''
    else:  # Number of Catches
        query = '''
            SELECT c.latitude, c.longitude, COUNT(c.catch_id) as catch_count
            FROM catches AS c
            GROUP BY c.batch_id, c.latitude, c.longitude
        '''

    # Execute query and read the result into a DataFrame
    df = pd.read_sql_query(query, connection)

    # Close the connection
    connection.close()

    return df


def create_heatmap(option):
    
    df = get_heatmap_data(option)
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
                            center=dict(lat=-40, lon=175), 
                            zoom=3,
                            mapbox_style="stamen-terrain", 
                            range_color=(1, max_catch_count))

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Set the bounds of the map to cover only the specific area of interest
    fig.update_geos(
        projection_type="mercator",
        lonaxis=dict(range=[150, 200]),
        lataxis=dict(range=[-43, -15])
    )

        # Set the size of the figure to be square
    fig.update_layout(
        mapbox_style="stamen-terrain",
        width=800,  # Width of the figure in pixels
        height=800  # Height of the figure in pixels
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
    dcc.Graph(id='heatmap')
])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('toggle-menu', 'value')]
)
def update_heatmap(selected_value):
    return create_heatmap(selected_value)

if __name__ == '__main__':

    app.run_server(debug=True)

