import psycopg2

class DatabaseCommunication:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

    def insert_statistics_row(self, statistics):
        query = """
        INSERT INTO statistics_table (statistics)
        VALUES (%s);
        """
        values = (statistics,)

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
        self.conn.commit()

    def insert_main_row(self, project, building, section, section_floor, flat, polygon_shape, video_url, statistics):
        # Insert statistics row
        self.insert_statistics_row(statistics)

        # Retrieve the ID of the inserted statistics row
        statistics_id = self.get_last_inserted_id('statistics_table')

        # Insert main row with the reference to statistics
        query = """
        INSERT INTO main_table (project, building, section, section_floor, flat, polygon_shape, video_url, statistics_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (project, building, section, section_floor, flat, polygon_shape, video_url, statistics_id)

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
        self.conn.commit()

    def retrieve_data(self, project=None, building=None, section=None, section_floor=None):
        query = """
        SELECT *
        FROM main_table
        WHERE (%s IS NULL OR project = %s)
        AND (%s IS NULL OR building = %s)
        AND (%s IS NULL OR section = %s)
        AND (%s IS NULL OR section_floor = %s);
        """
        values = (project, project, building, building, section, section, section_floor, section_floor)

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            rows = cursor.fetchall()
        return rows

    def get_last_inserted_id(self, table_name):
        query = f"SELECT currval(pg_get_serial_sequence('{table_name}', 'id'))"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            last_inserted_id = cursor.fetchone()[0]
        return last_inserted_id

    def close_connection(self):
        self.conn.close()
