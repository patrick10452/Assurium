import psycopg2
from typing import List, Tuple, Dict, Optional


class DataLoader:
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def load_all_data(self) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Load all data from the database and return structured collections
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Load books
                cursor.execute("""
                    SELECT book_id, title, author, genre, published_date 
                    FROM books
                """)
                books = [
                    {
                        'book_id': row[0],
                        'title': row[1],
                        'author': row[2],
                        'genre': row[3],
                        'published_date': row[4]
                    }
                    for row in cursor.fetchall()
                ]

                # Load chapters
                cursor.execute("""
                    SELECT chapter_id, book_id, chapter_number, title, content 
                    FROM chapters
                    ORDER BY chapter_number
                """)
                chapters = [
                    {
                        'chapter_id': row[0],
                        'book_id': row[1],
                        'chapter_number': row[2],
                        'title': row[3],
                        'content': row[4]
                    }
                    for row in cursor.fetchall()
                ]

                # Load paragraphs
                cursor.execute("""
                    SELECT paragraph_id, chapter_id, paragraph_number, content 
                    FROM paragraphs
                    ORDER BY paragraph_number
                """)
                paragraphs = [
                    {
                        'paragraph_id': row[0],
                        'chapter_id': row[1],
                        'paragraph_number': row[2],
                        'content': row[3]
                    }
                    for row in cursor.fetchall()
                ]

                return books, chapters, paragraphs
        finally:
            conn.close()