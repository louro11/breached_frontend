import os
import sqlite3


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        hash TEXT,
                        salt TEXT                 
                    )''')
    conn.commit()

# Function to insert data into the database
def insert_data(conn, data):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO data (
                        name, email, hash, salt
                    )
                    VALUES (?, ?, ?, ?)''', (data[1], data[2], data[3], data[4]))
    conn.commit()

def read_text_file(conn, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(":")
                if(len(data) > 4):
                    if (data[2] != "" or data[2] != " "):
                        insert_data(conn, data) 
                        #print(data)
    except FileNotFoundError:
        print("File not found.")


def main():
    folder_path = "..\Zomato_BF\Zomato_BF\data"
    if not os.path.isdir(folder_path):
        print("Invalid folder path!")
        return

    db_path = "zomato_breach.db"
    
    # Create SQLite database if it doesn't exist
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        create_table(conn)
        conn.close()
        print(f"SQLite database created at {db_path}")

    conn = sqlite3.connect(db_path)
    
    create_table(conn)
    file_path = folder_path + "\zomato.txt"
    read_text_file(conn, file_path)

    conn.close()
    print("Data insertion completed successfully.")

if __name__ == "__main__":
    main()