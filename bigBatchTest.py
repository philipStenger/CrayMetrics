# Check if the program can handle a large number of entries

import random
from crayfish_catch_management import Batch, Catch, create_database, insert_batch, retrieve_and_display_data, clear_database

def test_large_number_of_entries():
    # Create database
    create_database()

    # clear database
    clear_database()

    # Create a batch
    batch = Batch(BatchID='LargeBatch')

    # Add 100 catches to the batch
    for i in range(1, 101):
        catchID = f'C{i}'
        time = f"{random.randint(0,23)}:{random.randint(0,59):02}"
        coordinates = (round(random.uniform(-90, 90), 1), round(random.uniform(-180, 180), 1))
        weight = round(random.uniform(1, 10), 1)
        catch = Catch(catchID=catchID, time=time, coordinates=coordinates, weight=weight)
        batch.add_catch(catch)

    # Insert the batch into the database
    insert_batch(batch)

    # Display the batch data
    print("\nDisplaying data for LargeBatch:")
    retrieve_and_display_data('LargeBatch')

if __name__ == '__main__':
    # Execute the test
    test_large_number_of_entries()
