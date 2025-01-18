from flask import Flask, request, jsonify, render_template
from AssuriumChatbotProject.chatbot_engine import ChatbotEngine

app = Flask(__name__)
chatbot = ChatbotEngine()

# Root route to serve the index.html file
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot API endpoint
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