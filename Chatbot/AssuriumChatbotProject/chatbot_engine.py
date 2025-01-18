# AssuriumChatbotProject/chatbot_engine.py
from database import get_db_connection
import spacy
from fuzzywuzzy import process
from typing import List, Tuple, Dict, Optional
from models import Book, Chapter, Paragraph


class ChatbotEngine:
    def __init__(self):
        """Initialize the chatbot with enhanced search capabilities and NLU."""
        self.nlp = spacy.load("en_core_web_sm")  # Load a pre-trained NLP model
        self.context = {}  # Store conversation context
        self.keywords = {
            'book': ['book', 'title', 'author', 'about', 'tell me about', 'what is', 'genre'],
            'chapter': ['chapter', 'chapters', 'section'],
            'paragraph': ['paragraph', 'paragraphs', 'text', 'content'],
            'search': ['search', 'find', 'look for', 'where', 'what', 'how', 'tell me about'],
            'history': ['history', 'origin', 'evolution', 'background']
        }

    def extract_intent_and_entities(self, question: str) -> Tuple[Optional[str], List[Tuple[str, str]]]:
        """
        Extract intent and entities from the user's question using NLP.
        """
        doc = self.nlp(question)

        # Extract intent
        intent = None
        if any(keyword in question for keyword in self.keywords['book']):
            intent = "book"
        elif any(keyword in question for keyword in self.keywords['chapter']):
            intent = "chapter"
        elif any(keyword in question for keyword in self.keywords['paragraph']):
            intent = "paragraph"
        elif any(keyword in question for keyword in self.keywords['search']):
            intent = "search"
        elif any(keyword in question for keyword in self.keywords['history']):
            intent = "history"

        # Extract entities (e.g., chapter number, search terms)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return intent, entities

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a database query and return results."""
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

    def handle_history_question(self, question: str) -> str:
        """
        Handle questions about the history of insurance.
        """
        # Search for terms related to history in chapters and paragraphs
        query = """
            SELECT c.chapter_number, c.title, p.paragraph_number, p.content
            FROM paragraphs p
            JOIN chapters c ON p.chapter_id = c.chapter_id
            WHERE LOWER(p.content) LIKE LOWER(%s)
        """
        results = self.execute_query(query, ("%history%",))
        if results:
            response = "Here's what I found about insurance history:\n"
            for result in results:
                response += f"Chapter {result[0]}, Paragraph {result[2]}:\n{result[3][:200]}...\n\n"
            return response
        else:
            return "I couldn't find any information about insurance history."

    def process_question(self, question: str) -> str:
        """Process user questions and return appropriate responses."""
        question = question.lower().strip()

        # Extract intent and entities
        intent, entities = self.extract_intent_and_entities(question)

        try:
            # Handle specific intents
            if intent == "book":
                return self.handle_book_question()
            elif intent == "chapter":
                return self.handle_chapter_question(entities)
            elif intent == "paragraph":
                return self.handle_paragraph_question(entities)
            elif intent == "search":
                search_terms = [entity[0] for entity in entities]
                return self.smart_search(search_terms)
            elif intent == "history":
                return self.handle_history_question(question)
            else:
                return "I'm not sure what you're asking. Can you clarify?"

        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"

    def handle_book_question(self) -> str:
        """Handle questions about the book."""
        query = "SELECT title, author, genre, published_date FROM books WHERE book_id = 1"
        result = self.execute_query(query)
        if result:
            return f"Book Title: {result[0][0]}\nAuthor: {result[0][1]}\nGenre: {result[0][2]}\nPublished Date: {result[0][3]}"
        else:
            return "No book information found."

    def handle_chapter_question(self, entities: List[Tuple[str, str]]) -> str:
        """Handle questions about chapters."""
        chapter_number = None
        for entity in entities:
            if entity[1] == "CARDINAL":  # Extract chapter number from entities
                chapter_number = entity[0]
                break

        if chapter_number:
            query = "SELECT chapter_number, title, content FROM chapters WHERE chapter_number = %s"
            result = self.execute_query(query, (chapter_number,))
            if result:
                return f"Chapter {result[0][0]}: {result[0][1]}\nContent: {result[0][2][:200]}..."  # Show a snippet
            else:
                return f"Chapter {chapter_number} not found."
        else:
            return "Please specify a chapter number."

    def handle_paragraph_question(self, entities: List[Tuple[str, str]]) -> str:
        """Handle questions about paragraphs."""
        paragraph_number = None
        for entity in entities:
            if entity[1] == "CARDINAL":  # Extract paragraph number from entities
                paragraph_number = entity[0]
                break

        if paragraph_number:
            query = """
                SELECT p.paragraph_number, p.content, c.chapter_number
                FROM paragraphs p
                JOIN chapters c ON p.chapter_id = c.chapter_id
                WHERE p.paragraph_number = %s
            """
            result = self.execute_query(query, (paragraph_number,))
            if result:
                return f"Paragraph {result[0][0]} (Chapter {result[0][2]}): {result[0][1][:200]}..."  # Show a snippet
            else:
                return f"Paragraph {paragraph_number} not found."
        else:
            return "Please specify a paragraph number."