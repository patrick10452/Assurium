from database import get_db_connection
import re
from typing import List, Tuple, Dict, Optional


class ChatbotEngine:
    def __init__(self):
        """Initialize the chatbot with enhanced search capabilities"""
        self.keywords = {
            'book': ['book', 'title', 'author', 'about', 'tell me about', 'what is', 'genre'],
            'chapter': ['chapter', 'chapters', 'section'],
            'paragraph': ['paragraph', 'paragraphs', 'text', 'content'],
            'search': ['search', 'find', 'look for', 'where', 'what', 'how', 'tell me about']
        }

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a database query and return results"""
        conn = get_db_connection()
        if conn is None:
            raise Exception("Database connection failed")
        try:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def smart_search(self, search_terms: List[str]) -> str:
        """
        Enhanced search function that looks for terms across all tables
        and provides context-aware results
        """
        # Remove common words from search terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        search_terms = [term for term in search_terms if term.lower() not in common_words]

        if not search_terms:
            return "Please provide specific terms to search for."

        results = []

        # Create the LIKE patterns for each search term
        patterns = [f"%{term}%" for term in search_terms]

        # Search in books table
        book_query = """
            SELECT 'book' as source, title, author, genre, published_date
            FROM books
            WHERE LOWER(title) LIKE LOWER(%s)
               OR LOWER(author) LIKE LOWER(%s)
               OR LOWER(genre) LIKE LOWER(%s)
        """

        # Search in chapters table
        chapter_query = """
            SELECT 'chapter' as source, chapter_number, title, content
            FROM chapters
            WHERE LOWER(title) LIKE LOWER(%s)
               OR LOWER(content) LIKE LOWER(%s)
        """

        # Search in paragraphs table
        paragraph_query = """
            SELECT 'paragraph' as source, c.chapter_number, p.paragraph_number, p.content
            FROM paragraphs p
            JOIN chapters c ON p.chapter_id = c.chapter_id
            WHERE LOWER(p.content) LIKE LOWER(%s)
        """

        # Execute searches for each term
        for pattern in patterns:
            # Search in books
            book_results = self.execute_query(book_query, (pattern, pattern, pattern))
            for result in book_results:
                results.append({
                    'type': 'book',
                    'title': result[1],
                    'author': result[2],
                    'genre': result[3],
                    'date': result[4],
                    'term': pattern.strip('%')
                })

            # Search in chapters
            chapter_results = self.execute_query(chapter_query, (pattern, pattern))
            for result in chapter_results:
                results.append({
                    'type': 'chapter',
                    'chapter_num': result[1],
                    'title': result[2],
                    'content': result[3],
                    'term': pattern.strip('%')
                })

            # Search in paragraphs
            paragraph_results = self.execute_query(paragraph_query, (pattern,))
            for result in paragraph_results:
                results.append({
                    'type': 'paragraph',
                    'chapter_num': result[1],
                    'paragraph_num': result[2],
                    'content': result[3],
                    'term': pattern.strip('%')
                })

        if not results:
            return f"I couldn't find any information about: {', '.join(search_terms)}"

        # Format the results
        response = f"🔍 Here's what I found about: {', '.join(search_terms)}\n\n"

        # Group results by type
        if any(r['type'] == 'book' for r in results):
            response += "📚 Book Information:\n"
            for r in results:
                if r['type'] == 'book':
                    response += f"Found '{r['term']}' in:\n"
                    response += f"Title: {r['title']}\n"
                    response += f"Author: {r['author']}\n"
                    response += f"Genre: {r['genre']}\n"
                    response += f"Published: {r['date']}\n\n"

        if any(r['type'] == 'chapter' for r in results):
            response += "📑 Chapter Matches:\n"
            for r in results:
                if r['type'] == 'chapter':
                    response += f"Found '{r['term']}' in Chapter {r['chapter_num']}: {r['title']}\n"
                    # Get a snippet of content around the search term
                    content = r['content'].lower()
                    term_pos = content.find(r['term'].lower())
                    if term_pos != -1:
                        start = max(0, term_pos - 50)
                        end = min(len(content), term_pos + len(r['term']) + 50)
                        snippet = "..." + content[start:end] + "...\n"
                        response += f"Context: {snippet}\n"

        if any(r['type'] == 'paragraph' for r in results):
            response += "📝 Paragraph Matches:\n"
            for r in results:
                if r['type'] == 'paragraph':
                    response += f"Found '{r['term']}' in Chapter {r['chapter_num']}, Paragraph {r['paragraph_num']}\n"
                    # Get a snippet of content around the search term
                    content = r['content'].lower()
                    term_pos = content.find(r['term'].lower())
                    if term_pos != -1:
                        start = max(0, term_pos - 50)
                        end = min(len(content), term_pos + len(r['term']) + 50)
                        snippet = "..." + content[start:end] + "...\n"
                        response += f"Context: {snippet}\n"

        return response

    def process_question(self, question: str) -> str:
        """Process user questions and return appropriate responses"""
        question = question.lower().strip()

        # Extract search terms
        words = question.split()
        search_terms = [word for word in words if len(word) > 2]  # Only consider words longer than 2 characters

        try:
            # If the question contains search keywords or doesn't match other patterns,
            # treat it as a search query
            if (any(keyword in question for keyword in self.keywords['search']) or
                    not any(keyword in question for keyword in sum(self.keywords.values(), []))):
                return self.smart_search(search_terms)

            # Handle other specific queries (book info, chapters, paragraphs)
            # [Previous code for handling specific queries remains the same]

        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"

        return "I'm not sure what you're asking. Try asking about specific content or use search terms."