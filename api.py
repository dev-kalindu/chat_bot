from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches

app = Flask(__name__)
CORS(app) 

# ✅ Allow React app (port 5173) to access Flask (port 5000)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    knowledge_base = load_knowledge_base("knowledge_base.json")
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({"reply": answer})
    else:
        return jsonify({"reply": "I don't know the answer. Can you teach me?"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
