# Crayfish Catch Management Program

This Python program provides a comprehensive solution to manage and visualize crayfish catches. It interfaces with an SQLite database to manage batches and individual catches, and leverages Plotly for data visualization.

## Import Statements

The code imports various libraries and modules necessary for its functions:

- `random` for generating random values.
- `sqlite3` for interacting with the SQLite database.
- `datetime` and `timedelta` for handling date and time-related operations.
- `pandas` as `pd` for handling data.
- `plotly.express` as `px` for plotting data.
- Specific functions and classes from a custom module `crayfish_catch_management`.

## Functions

### generate_and_insert_data

This function generates and inserts 20 batches of data into the crayfish catch database. It uses random values to create unique catches and links them to specific batches. It handles connecting to the database, iterating through the batches, and managing the catches' details.

### populate_large_database

This function populates the database with 20 batches, each containing 10 to 20 catches. It uses random values for the attributes of the catches and inserts the batches into the database.

### get_scatter_data

This function retrieves data for a scatter plot from the database. It connects to the SQLite database, executes a select query to fetch latitude and longitude, and returns the result as a Pandas DataFrame.

### get_bar_data

This function retrieves data for a bar plot from the database. It joins batches and catches tables and groups by batch_id to calculate the total weight of catches per batch. It returns the result as a Pandas DataFrame.

## Main Function

The `main` function coordinates the program's flow:

1. **Clear Database**: Clears any existing data in the database.
2. **Create Database**: Calls the `create_database` function to ensure database structure is in place.
3. **Populate Database**: Calls the `generate_and_insert_data` function to populate the database with data.
4. **Retrieve and Display Data**: Demonstrates how to retrieve and display specific data from the database.
5. **Scatter Plot**: Plots catch locations using Plotly.
6. **Bar Plot**: (Commented out) Plots the total weight of catches per batch using Plotly.

## Usage

When run as a standalone script, the program executes the `main` function, performing all the described steps. The code provides insights into managing crayfish catches using Python, SQLite, and data visualization tools.

## Notes

- The `crayfish_catch.db` file is automatically created if it doesn't exist.
- The code requires the SQLite library and Plotly to be installed in the environment.
- The `crayfish_catch_management` module should be properly defined with required classes and functions as imported in the script.
