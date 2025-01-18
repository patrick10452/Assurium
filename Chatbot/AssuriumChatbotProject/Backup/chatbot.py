from chatbot_engine import ChatbotEngine
import time


def display_welcome_message():
    """Display a welcoming message with loading animation"""
    print("\n=== Insurance Book Chatbot ===")
    print("Initializing", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")


def run_chatbot():
    """Run the chatbot interaction loop"""
    try:
        display_welcome_message()
        chatbot = ChatbotEngine()

        print("🤖 Welcome! I'm your Insurance Book Assistant!")
        print("\nYou can ask me about:")
        print("📚 Book information - 'Tell me about the book'")
        print("📑 Chapters - 'Show all chapters' or 'Tell me about chapter 1'")
        print("📝 Paragraphs - 'Show paragraphs in chapter 1'")
        print("🔍 Search - 'Search for insurance claims'")
        print("\nType 'exit' to quit.")

        while True:
            try:
                user_input = input("\n❓ You: ").strip()

                if not user_input:
                    print("Please type your question.")
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Goodbye! Have a great day!")
                    break

                print("\n🤖 Assistant:", end=" ")
                response = chatbot.process_question(user_input)
                print(response)

            except Exception as e:
                print("\n❌ Sorry, I encountered an error. Please try asking your question differently.")
                print(f"Error details: {str(e)}")

    except Exception as e:
        print(f"\n❌ Failed to initialize chatbot: {str(e)}")


if __name__ == "__main__":
    run_chatbot()