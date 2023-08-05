# checks if database is running smoothly

import unittest
import sqlite3
from crayfish_catch_management import Catch, Batch, create_database, insert_batch, remove_batch

class TestCrayfishCatchManagement(unittest.TestCase):

    def test_create_database(self):
        create_database()
        connection = sqlite3.connect('crayfish_catch.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.assertIn(('batches',), tables)
        self.assertIn(('catches',), tables)
        connection.close()

    def test_insert_and_retrieve_data(self):
        # Create sample data
        catch1 = Catch(catchID='CT1', time='12:30', coordinates=(42.3601, -71.0589), weight=5.2)
        batch1 = Batch(BatchID='BT1')
        batch1.add_catch(catch1)

        # Insert batch
        insert_batch(batch1)

        # Retrieve and validate
        connection = sqlite3.connect('crayfish_catch.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM batches WHERE batch_id = ?', ('BT1',))
        batch_data = cursor.fetchone()
        self.assertIsNotNone(batch_data)

        cursor.execute('SELECT * FROM catches WHERE catch_id = ?', ('CT1',))
        catch_data = cursor.fetchone()
        self.assertIsNotNone(catch_data)
        connection.close()

    def test_remove_batch(self):
        # Create sample data
        catch1 = Catch(catchID='CT2', time='13:30', coordinates=(43.3601, -72.0589), weight=6.2)
        batch1 = Batch(BatchID='BT2')
        batch1.add_catch(catch1)

        # Insert batch
        insert_batch(batch1)

        # Remove batch
        remove_batch('BT2')

        # Validate removal
        connection = sqlite3.connect('crayfish_catch.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM batches WHERE batch_id = ?', ('BT2',))
        self.assertIsNone(cursor.fetchone())

        cursor.execute('SELECT * FROM catches WHERE catch_id = ?', ('CT2',))
        self.assertIsNone(cursor.fetchone())
        connection.close()

    def test_retrieve_non_existing_batch(self):
        # Retrieve non-existing batch
        connection = sqlite3.connect('crayfish_catch.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM batches WHERE batch_id = ?', ('NonExist',))
        self.assertIsNone(cursor.fetchone())
        connection.close()

if __name__ == '__main__':
    # Start by creating the database tables
    create_database()
    unittest.main()
