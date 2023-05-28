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

    def insert_main_row(self, project_slug, building_pk, section_id, section_floor, flat_id, polygon_shape, video_url, completion_percentage):
        # Insert main row with the reference to statistics
        query = """
        INSERT INTO statistics (project, building, section, section_floor, flat, polygon_shape, video_url, completion_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (project_slug, building_pk, section_id, section_floor, flat_id, polygon_shape, video_url, completion_percentage)

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
        self.conn.commit()

    def retrieve_data(self, project_slug=None, building_pk=None, section_id=None, section_floor=None):
        query = """
        SELECT *
        FROM main_table
        WHERE (%s IS NULL OR project = %s)
        AND (%s IS NULL OR building = %s)
        AND (%s IS NULL OR section = %s)
        AND (%s IS NULL OR section_floor = %s);
        """
        values = (project_slug, project_slug, building_pk, building_pk, section_id, section_id, section_floor, section_floor)

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            rows = cursor.fetchall()
        return rows


    def close_connection(self):
        self.conn.close()
