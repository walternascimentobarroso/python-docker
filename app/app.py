from flask import Flask, request, jsonify
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
db = Database(os.getenv('MONGODB_URI'), os.getenv('DB_NAME'), os.getenv('COLLECTION_NAME'))

@app.route('/')
def hello():
    return 'Hello, world!'

# Rotas da API
@app.route('/quiz', methods=['GET'])
def get_quiz():
    quiz_data = db.get_quiz_data()
    return jsonify({"quiz": quiz_data})

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    submitted_answers = request.json.get("answers", [])
    score = sum(1 for submitted, correct in zip(submitted_answers, db.get_correct_answers()) if submitted == correct)
    return jsonify({"score": score})

@app.route('/quiz/add', methods=['POST'])
def add_quiz():
    new_question = request.json.get("question", {})
    db.insert_question(new_question)
    return jsonify({"message": "Questão adicionada com sucesso!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

