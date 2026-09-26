import sqlite3
import pandas as pd
import os


# File locations
CSV_PATH = "data/bugs.csv"
DB_PATH = "database/bugs.db"


def create_database():

    # Make database folder if it doesn't exist
    os.makedirs("database", exist_ok=True)

    # Read CSV
    df = pd.read_csv(CSV_PATH)

    # Connect to SQLite
    connection = sqlite3.connect(DB_PATH)

    # Store CSV data in SQLite table
    df.to_sql(
        "bugs",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("Database created successfully!")
    print(f"Total bugs inserted: {len(df)}")


def get_all_bugs():

    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM bugs",
        connection
    )

    connection.close()

    return df


# Run database creation
if __name__ == "__main__":
    create_database()