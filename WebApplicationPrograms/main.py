import dash
from dash import html
from dash.dependencies import Input, Output
from db_utils import get_time_series_data
from plot_utils import create_heatmap
from app_utils import create_title, create_configuration, create_heatmap_and_timeseries
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def app_layout(app):
    app.layout = html.Div([
    create_title(),
    create_configuration(),
    create_heatmap_and_timeseries(),
])
    
def register_callbacks(app):
    @app.callback(
    Output('heatmap', 'figure'),
    [Input('toggle-menu', 'value'),
     Input('lat_min', 'value'),
     Input('lat_max', 'value'),
     Input('lon_min', 'value'),
     Input('lon_max', 'value'),
     Input('time-interval', 'value'),
     Input('start-date', 'date'),  
     Input('end-date', 'date')] )
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
     Input('start-date', 'date'),  
     Input('end-date', 'date')]  )
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

def main():
    app = dash.Dash(__name__)
    app_layout(app)
    register_callbacks(app)
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
