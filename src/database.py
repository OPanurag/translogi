import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    """
    Ensure the `translogi` database and `delivery` table exist.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS translogi")

            # Switch to the database
            cursor.execute("USE translogi")

            # Create the delivery table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS delivery (
                    Store_Latitude FLOAT NOT NULL,
                    Store_Longitude FLOAT NOT NULL,
                    Drop_Latitude FLOAT NOT NULL,
                    Drop_Longitude FLOAT NOT NULL,
                    Delivery_Time INT NOT NULL
                )
            """)
            connection.commit()

            print("Database and table ensured.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def load_and_clean_data(file_path):
    """
    Load and clean data from a CSV file.
    """
    df = pd.read_csv(file_path)

    # Select relevant columns
    selected_columns = df[['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude', 'Delivery_Time']]

    # Drop rows with NaN values and reset index
    selected_columns = selected_columns.dropna().reset_index(drop=True)

    return selected_columns

def insert_dataframe_to_mysql(df, table_name):
    """
    Insert a pandas DataFrame into a MySQL table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database="translogi"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Prepare SQL INSERT query
            cols = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            # Convert DataFrame to list of tuples
            data = [tuple(row) for row in df.values]

            cursor.executemany(sql, data)
            connection.commit()

            print(f"{cursor.rowcount} records inserted into {table_name}.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def save_cleaned_data(df, output_path):
    """
    Save the cleaned DataFrame to a CSV file.
    """
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}.")

def main():
    """
    Main function to handle the entire process.
    """
    file_path = 'data/amazon_delivery.csv'  # Path to the original CSV file
    output_path = 'data/cleaned_amazon_delivery.csv'  # Path to save the cleaned CSV
    table_name = 'delivery'

    # Set MySQL credentials in environment variables
    os.environ["MYSQL_USER"] = "" # Add your MySQL username
    os.environ["MYSQL_PASSWORD"] = "" # Add your MySQL password

    # Step 1: Ensure database and table exist
    create_database_and_table()

    # Step 2: Load and clean data
    cleaned_data_df = load_and_clean_data(file_path)

    # Step 3: Insert cleaned data into MySQL
    insert_dataframe_to_mysql(cleaned_data_df, table_name)

    # Step 4: Save cleaned data back to CSV
    save_cleaned_data(cleaned_data_df, output_path)

if __name__ == "__main__":
    main()
