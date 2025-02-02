import pandas as pd
import mysql.connector as mysql

# 1. Load the spreadsheet.
file_path = '/absolute/path/to/spreadsheet.xlsx'
sheet_name = 'Sheet1'   # Sheet name (currently default).

df = pd.read_excel(file_path, sheet_name, dtype=str)

# 2. Connect to MySQL.
db = mysql.connect(
    host="localhost",   # Currently default (will work as-is). Either replace or optionally add a specific port if not on the default 3306.
    user="user",    # Replace with your MySQL username.
    password="password",   # Replace with your MySQL password.
    database="database"    # Replace with your MySQL database name.
)

cursor = db.cursor()

# 3. Create table if it doesn't exist.
table_name = 'CourseData'
columns = ", ".join([f"{col} VARCHAR(255)" for col in df.columns])  # Assuming all columns as VARCHAR.

create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
cursor.execute(create_table_query)

# 4. Insert data into the table.
insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s' for _ in df.columns])})"
data = [tuple(row) for row in df.values]
cursor.executemany(insert_query, data)
db.commit()

# 5. Close the connection.
cursor.close()
db.close()

print(f"Data from {file_path} has been successfully inserted into the table '{table_name}' in the MySQL database.")
