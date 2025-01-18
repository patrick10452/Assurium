from AssuriumChatbotProject.chatbot_engine import ChatbotEngine
from flask import Flask, request, jsonify

app = Flask(__name__)
chatbot = ChatbotEngine()

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to handle chatbot interactions.
    """
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"response": "Please provide a question."}), 400

    response = chatbot.process_question(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)