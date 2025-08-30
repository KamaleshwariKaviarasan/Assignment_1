import pandas as pd
import mysql.connector

# MySQL connection details (only server, no db yet)
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root@localhost",
    "password": "Kamale@05"
}

DB_NAME = "imdb_details"
TABLE_NAME = "imdb_table"


def create_database_if_not_exists():
    try:
        conn = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="G3EycSwv11HRaoP.root",
            password="fXvnUBohq2ZcrRbU",
            port = 4000,
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.close()
    except Exception as e:
        print(e)


def create_table_if_not_exists(df):
    conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
    cursor = conn.cursor()

    # Build table schema dynamically from Excel columns
    columns = []
    for col in df.columns:
        colname = col.strip().replace(" ", "_")  # clean name
        columns.append(f"{colname} VARCHAR(500)")

    schema = ", ".join(columns)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {schema}
        )
    """)

    conn.close()


def insert_data_from_excel(excel_file):
    # Read Excel
    df = pd.read_excel(excel_file)

    # Step 1: Create DB if not exists
    create_database_if_not_exists()

    # Step 2: Create table if not exists (with Excel columns)
    create_table_if_not_exists(df)

    # Step 3: Insert data
    conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cols = ", ".join([f"{col.strip().replace(' ', '_')}" for col in df.columns])
        placeholders = ", ".join(["%s"] * len(df.columns))
        values = tuple(row[col] for col in df.columns)

        cursor.execute(
            f"INSERT INTO {TABLE_NAME} ({cols}) VALUES ({placeholders})",
            values
        )

    conn.commit()
    conn.close()
    print("✅ Excel data inserted successfully!")


if __name__ == "__main__":
    insert_data_from_excel("imdb_movies_2024.xlsx")  