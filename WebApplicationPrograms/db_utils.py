import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "DatabasePrograms/crayfish_catch.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

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
