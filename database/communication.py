import sqlite3

class DatabaseCommunication:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        """
        Create a table in the database to store flat statistics if it doesn't already exist.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flat_statistics (
                flat_id INTEGER PRIMARY KEY,
                area FLOAT,
                price FLOAT
            )
        ''')

        conn.commit()
        conn.close()

    def insert_statistics(self, flat_id, area, price):
        """
        Insert statistics about a flat into the database.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Insert the statistics into the table
        cursor.execute('''
            INSERT INTO flat_statistics (flat_id, area, price)
            VALUES (?, ?, ?)
        ''', (flat_id, area, price))

        conn.commit()
        conn.close()
