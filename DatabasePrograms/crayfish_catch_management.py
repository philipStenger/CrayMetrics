import sqlite3

def create_database():
    # Connect to SQLite database (it will create the file if not exists)
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    # Create tables for Batch and Catch
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batches (
            batch_id TEXT PRIMARY KEY,
            weight REAL,
            number INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catches (
            catch_id TEXT PRIMARY KEY,
            batch_id TEXT,
            time TIMESTAMP,
            latitude REAL,
            longitude REAL,
            weight REAL,
            FOREIGN KEY (batch_id) REFERENCES batches (batch_id)
        )
    ''')

    # Commit and close connection
    connection.commit()
    connection.close()

def insert_batch(batch):
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO batches (batch_id, weight, number) VALUES (?, ?, ?)', 
                   (batch.BatchID, batch.batchWeight, batch.batchNumber))

    # Insert related catches
    for catch in batch.catches.values():
        insert_catch(cursor, batch.BatchID, catch)

    connection.commit()
    connection.close()

def insert_catch(cursor, batch_id, catch):
    cursor.execute('INSERT INTO catches (catch_id, batch_id, time, latitude, longitude, weight) VALUES (?, ?, ?, ?, ?, ?)',
                   (catch.catchID, batch_id, catch.time.strftime('%Y-%m-%d %H:%M:%S'), catch.coordinates[0], catch.coordinates[1], catch.weight))

def remove_batch(batch_id):
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    # Delete the catches related to the batch
    cursor.execute('DELETE FROM catches WHERE batch_id = ?', (batch_id,))

    # Delete the batch itself
    cursor.execute('DELETE FROM batches WHERE batch_id = ?', (batch_id,))

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

    print(f'Batch {batch_id} and related catches have been removed.')

def clear_database():
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    # Delete all records from the catches table
    cursor.execute('DELETE FROM catches')

    # Delete all records from the batches table
    cursor.execute('DELETE FROM batches')

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

    print('Database has been cleared.')

def retrieve_and_display_data(batch_id):
    # Connect to the database
    connection = sqlite3.connect('crayfish_catch.db')
    cursor = connection.cursor()

    # Retrieve batch information
    cursor.execute('SELECT * FROM batches WHERE batch_id = ?', (batch_id,))
    batch_data = cursor.fetchone()
    if batch_data:
        print('='*55)
        print(f'BatchID: {batch_data[0]}, Total Weight: {batch_data[1]}, Number of Catches: {batch_data[2]}')
        print('='*55)
    else:
        print(f'Batch with ID {batch_id} not found.')
        return

    # Retrieve catches related to the batch
    cursor.execute('SELECT * FROM catches WHERE batch_id = ?', (batch_id,))
    catches = cursor.fetchall()

    # Print table headers
    print('CatchID\tTime\tCoordinates\t\tWeight')
    print('='*55)

    # Print details of catches
    for catch in catches:
        catch_id, _, time, latitude, longitude, weight = catch
        coordinates = f'({latitude}, {longitude})'
        print(f'{catch_id}\t{time}\t{coordinates}\t{weight}')

    # Close the connection
    connection.close()

class Catch:
    def __init__(self, catchID, time, coordinates, weight):
        self.catchID = catchID
        self.time = time
        self.coordinates = coordinates  # Tuple or dictionary containing latitude and longitude
        self.weight = weight

    def __str__(self):
        return f'Catch(catchID={self.catchID}, time={self.time}, coordinates={self.coordinates}, weight={self.weight})'

    def __repr__(self):
        return self.__str__()

class Batch:
    def __init__(self, BatchID):
        self.BatchID = BatchID
        self.batchWeight = 0
        self.batchNumber = 0
        self.catches = {} # Dictionary to store Catch objects by their catchID

    def add_catch(self, catch):
        if catch.catchID in self.catches:
            raise ValueError(f"Catch with ID {catch.catchID} already exists in this batch")
        
        self.catches[catch.catchID] = catch
        self.batchNumber += 1
        self.batchWeight += catch.weight

    def remove_catch(self, catchID):
        if catchID not in self.catches:
            raise KeyError(f"No catch with ID {catchID} found in this batch")
        
        catch = self.catches.pop(catchID)
        self.batchNumber -= 1
        self.batchWeight -= catch.weight

    def __str__(self):
        return f'Batch(BatchID={self.BatchID}, batchWeight={self.batchWeight}, batchNumber={self.batchNumber}, catches={self.catches})'

    def __repr__(self):
        return self.__str__()
    
def main():

    create_database()

    # # Create Catch objects
    # catch1 = Catch(catchID='C1', time='12:30', coordinates=(42.3601, -71.0589), weight=5.2)
    # catch2 = Catch(catchID='C2', time='13:15', coordinates=(40.7128, -74.0060), weight=6.3)
    # catch3 = Catch(catchID='C3', time='09:45', coordinates=(34.0522, -118.2437), weight=4.7)
    # catch4 = Catch(catchID='C4', time='10:00', coordinates=(37.7749, -122.4194), weight=7.0)
    # catch5 = Catch(catchID='C5', time='14:30', coordinates=(51.5074, -0.1278), weight=3.9)
    
    # # Create Batch 1 and add catches
    # batch1 = Batch(BatchID='B1')
    # batch1.add_catch(catch1)
    # batch1.add_catch(catch2)

    # # Create Batch 2 and add catches
    # batch2 = Batch(BatchID='B2')
    # batch2.add_catch(catch3)
    # batch2.add_catch(catch4)

    # # Create Batch 3 and add catches
    # batch3 = Batch(BatchID='B3')
    # batch3.add_catch(catch5)

    # Insert batches into database
    # insert_batch(batch1)
    # insert_batch(batch2)
    # insert_batch(batch3)

    # Remove batch from database
    # remove_batch('B3')
    # remove_batch('B2')
    # remove_batch('B1')

    # Retrieve and display data
    # retrieve_and_display_data('B1')

if __name__ == '__main__':
    main()



