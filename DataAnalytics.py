import random
from crayfish_catch_management import Batch, Catch, create_database, insert_batch, insert_catch, retrieve_and_display_data, clear_database
import plotly.express as px
import sqlite3
import pandas as pd

import random
from datetime import datetime, timedelta

def generate_and_insert_data():
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    # Iterate through 20 batches
    for batch_number in range(1, 101):
        batch_id = f'B{batch_number}'
        num_catches = random.randint(20, 50)
        base_time = datetime(2023, 1, 1, random.randint(0, 23), 0)
        base_latitude = random.uniform(-53, -25)
        base_longitude = random.uniform(160, 190)
        
        # Create and insert batch
        batch = Batch(BatchID=batch_id)
        cursor.execute('INSERT INTO batches (batch_id, weight, number) VALUES (?, ?, ?)', (batch.BatchID, 0, num_catches))

        # Generate and insert catches for the batch
        for catch_number in range(1, num_catches + 1):
            time_variance = timedelta(minutes=random.randint(-30, 30))
            time = (base_time + time_variance).strftime('%H:%M')
            latitude = round(base_latitude + random.uniform(-0.25, 0.25), 1)
            longitude = round(base_longitude + random.uniform(-0.25, 0.25), 1)
            weight = round(random.uniform(2, 5), 1)

            catch_id = f'{time}/B{batch_number}/C{catch_number}'
            catch = Catch(catchID=catch_id, time=time, coordinates=(latitude, longitude), weight=weight)
            batch.add_catch(catch)
            insert_catch(cursor, batch_id, catch) # Insert the catch into the database

        # Update batch weight
        cursor.execute('UPDATE batches SET weight = ? WHERE batch_id = ?', (batch.batchWeight, batch_id))

    # Commit and close connection
    connection.commit()
    connection.close()

    print('Data generation and insertion complete.')

def populate_large_database():
    # Create 20 batches with 10 to 20 catches each
    batches = []
    for batch_number in range(20):
        num_catches = random.randint(10, 20) # Randomly choose number of catches between 10 to 20
        batch = Batch(BatchID=f'B{batch_number}')
        for catch_number in range(num_catches):
            time = f"{random.randint(0, 23)}:{str(random.randint(0, 59)).zfill(2)}"
            latitude = round(random.uniform(-90, 90), 1)
            longitude = round(random.uniform(-180, 180), 1)
            weight = round(random.uniform(1, 10), 1)
            catch = Catch(catchID=f'{time}/B{batch_number}/C{catch_number}', time=time, coordinates=(latitude, longitude), weight=weight)
            batch.add_catch(catch)
        batches.append(batch)

    # Insert batches into the database
    for batch in batches:
        insert_batch(batch)

    print(f"Successfully inserted {len(batches)} batches into the database.")

# Function to retrieve data for scatter plot
def get_scatter_data():
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()
    cursor.execute('SELECT latitude, longitude FROM catches')
    data = cursor.fetchall()
    connection.close()
    return pd.DataFrame(data, columns=['Latitude', 'Longitude'])

# Function to retrieve data for bar plot
def get_bar_data():
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()
    cursor.execute('SELECT batches.batch_id, SUM(catches.weight) FROM batches LEFT JOIN catches ON batches.batch_id = catches.batch_id GROUP BY batches.batch_id')
    data = cursor.fetchall()
    connection.close()
    return pd.DataFrame(data, columns=['BatchID', 'Total Weight'])

def main():

    # clear database
    clear_database()

    # Create database
    create_database()

    # Populate database with 20 batches with 10 to 20 catches each
    generate_and_insert_data()
    # populate_large_database()

    retrieve_and_display_data('B1')

    # Scatter Plot
    # scatter_data = get_scatter_data()
    # scatter_fig = px.scatter(scatter_data, x='Latitude', y='Longitude', title='Catch Locations')
    # scatter_fig.show()

    # Bar Plot
    # bar_data = get_bar_data()
    # bar_fig = px.bar(bar_data, x='BatchID', y='Total Weight', title='Total Weight of Catches per Batch')
    # bar_fig.show()

if __name__ == '__main__':
    main()
