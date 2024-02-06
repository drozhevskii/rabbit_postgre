import psycopg2
from config import load_config

def create_tables():

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY,
            image_name VARCHAR(255) NOT NULL,
            image_status VARCHAR(255) NOT NULL,
            date_processed TIMESTAMP
        )
        ''')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()