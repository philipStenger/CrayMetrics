Overview
This code defines a simple system to manage crayfish catches and batch them together. It leverages SQLite to store batches and individual catches, providing functionality to create, insert, remove, clear, and retrieve data from the database. It consists of a set of functions to perform these tasks and two classes to represent a catch and a batch.

Classes
Catch
Attributes:
- catchID: A unique identifier for the catch.
- time: The time the catch was made.
- coordinates: A tuple containing latitude and longitude.
- weight: The weight of the catch.

Batch
Attributes:
- BatchID: A unique identifier for the batch.
- batchWeight: The total weight of the catches in the batch.
- batchNumber: The total number of catches in the batch.
- catches: A dictionary storing Catch objects by their catchID.

Methods:
- add_catch(catch): Adds a catch to the batch.
- remove_catch(catchID): Removes a catch from the batch.

Functions
- create_database(): Purpose: Creates the SQLite database and tables for batches and catches if they don't exist.
- insert_batch(batch): Purpose: Inserts a Batch object and its related Catch objects into the database. Parameters: batch: A Batch object.
- insert_catch(cursor, batch_id, catch): Purpose: Inserts a Catch object into the database. Parameters: cursor: An SQLite cursor object; batch_id: The associated batch ID; catch: A Catch object.
- remove_batch(batch_id): Purpose: Removes a batch and its related catches from the database. Parameters: batch_id: The ID of the batch to be removed.
- clear_database(): Purpose: Clears all records from both the batches and catches tables in the database.
- retrieve_and_display_data(batch_id): Purpose: Retrieves and prints the details of a batch and its related catches from the database. Parameters: batch_id: The ID of the batch to be retrieved.

Usage
The main() function at the bottom demonstrates the usage of these functions and classes. It shows how to create Catch and Batch objects, add catches to batches, and interact with the database.

Notes
- Make sure the SQLite library is installed in your environment as the code depends on it.
- The database file crayfish_catch.db is automatically created if it doesn't exist.
- Ensure unique catch and batch IDs to prevent integrity errors in the database.
- The provided code snippet doesn't include calls to insert or remove batches in the main() function (they're commented out), so uncomment those lines as needed in your application.
