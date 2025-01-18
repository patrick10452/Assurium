# AssuriumChatbotProject/models.py
from AssuriumChatbotProject.database import get_db_connection

class Book:
    @staticmethod
    def get_book_info():
        """
        Fetch book information from the database.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT title, author, genre, published_date FROM books WHERE book_id = 1")
        book_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return book_info

class Chapter:
    @staticmethod
    def get_all_chapters():
        """
        Fetch all chapters from the database.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT chapter_number, title, content FROM chapters WHERE book_id = 1")
        chapters = cursor.fetchall()
        cursor.close()
        conn.close()
        return chapters

class Paragraph:
    @staticmethod
    def get_paragraphs_by_chapter(chapter_id):
        """
        Fetch all paragraphs for a specific chapter.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT paragraph_number, content FROM paragraphs WHERE chapter_id = %s", (chapter_id,))
        paragraphs = cursor.fetchall()
        cursor.close()
        conn.close()
        return paragraphs