# AssuriumChatbotProject/utils.py
from models import Book, Chapter, Paragraph

def process_question(question):
    """
    Process the user's question and return an appropriate response.
    """
    question = question.lower()

    if "book" in question or "title" in question or "author" in question:
        book_info = Book.get_book_info()
        if book_info:
            return f"Book Title: {book_info[0]}\nAuthor: {book_info[1]}\nGenre: {book_info[2]}\nPublished Date: {book_info[3]}"
        else:
            return "No book information found."

    elif "chapter" in question:
        chapters = Chapter.get_all_chapters()
        if chapters:
            response = "Chapters in the book:\n"
            for chapter in chapters:
                response += f"Chapter {chapter[0]}: {chapter[1]}\nContent: {chapter[2]}\n\n"
            return response
        else:
            return "No chapters found."

    elif "paragraph" in question:
        paragraphs = Paragraph.get_paragraphs_by_chapter(1)  # Assuming Chapter 1 for now
        if paragraphs:
            response = "Paragraphs in Chapter 1:\n"
            for paragraph in paragraphs:
                response += f"Paragraph {paragraph[0]}: {paragraph[1]}\n\n"
            return response
        else:
            return "No paragraphs found."

    else:
        return "I'm sorry, I don't understand your question. Please ask about the book, chapters, or paragraphs."