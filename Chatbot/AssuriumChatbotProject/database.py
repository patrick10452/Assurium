import psycopg2
from psycopg2 import OperationalError

# Connection parameters
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5432",
    "dbname": "test_env",
    "user": "postgres",
    "password": "@SsUr!m.2024?"  # Replace with your actual password
}


def get_db_connection():
    """
    Create and return a database connection.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None


# Database initialization script
def init_database():
    """
    Initialize the database with required tables.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            # Create books table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    genre VARCHAR(100),
                    published_date DATE
                )
            """)

            # Create chapters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    chapter_id SERIAL PRIMARY KEY,
                    book_id INTEGER REFERENCES books(book_id),
                    chapter_number INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content TEXT
                )
            """)

            # Create paragraphs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paragraphs (
                    paragraph_id SERIAL PRIMARY KEY,
                    chapter_id INTEGER REFERENCES chapters(chapter_id),
                    paragraph_number INTEGER NOT NULL,
                    content TEXT
                )
            """)

            conn.commit()
            return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()