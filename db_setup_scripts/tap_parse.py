import os
import sqlite3

unique_lines = set()
# Function to create database table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        id INTEGER PRIMARY KEY,
                        full_name TEXT,
                        email TEXT,
                        phone_number TEXT,
                        date_of_birth TEXT,                 
                        gender TEXT,
                        country TEXT,
                        address TEXT,
                        city TEXT,                          
                        postal_code TEXT
                    )''')
    conn.commit()

# Function to insert data into the database
def insert_data(conn, data):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO data (
                        full_name, email, phone_number, date_of_birth, gender, country, address, city, postal_code
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (data[6], data[14], data[26], data[1], data[8], data[10], data[11], data[9] , data[13]))
    conn.commit()

def process_csv_file(file_path, conn):
    with open(file_path, 'r', encoding='ISO 8859-15') as csv_file:
        lines = csv_file.readlines()[1:]
        for line in lines:
            # Remove quotes
            line = line.replace('"', '')
            # Split the line into fields
            data = line.strip().split('|')
            #print(data)
            if tuple(data[14]) not in unique_lines:
                insert_data(conn, data)
                unique_lines.add(tuple(data[14]))

# Function to process all CSV files in a folder
def process_csv_files(folder_path, conn):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            process_csv_file(file_path, conn)

# Main function
def main():
    folder_path = "..\TAPAir_BF\TAPAir_BF\data"
    if not os.path.isdir(folder_path):
        print("Invalid folder path!")
        return

    db_path = "tap_breach.db"
    
    # Create SQLite database if it doesn't exist
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        create_table(conn)
        conn.close()
        print(f"SQLite database created at {db_path}")

    conn = sqlite3.connect(db_path)
    
    create_table(conn)
    process_csv_files(folder_path, conn)

    conn.close()
    print("Data insertion completed successfully.")

if __name__ == "__main__":
    main()

