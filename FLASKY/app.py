from flask import Flask, request, jsonify
from chatbot import FinanceKnowledgeBot

app = Flask(__name__)
bot = FinanceKnowledgeBot("financial_and_stock_queries_1000.csv")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input.strip():
        return jsonify({"response": "Please ask a question."}), 400
    response = bot.get_response(user_input)
    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def home():
    return " Finance Chatbot API is running!"

if __name__ == "__main__":
    app.run(debug=True)

