# Purpose: Convert SQLite database to Excel file

import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('DatabasePrograms\crayfish_catch.db')

# Read a table into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM catches", conn)

# Save to Excel
df.to_excel('output\output_catches.xlsx', index=False)

# Don't forget to close the connection
conn.close()
