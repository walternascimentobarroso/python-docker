from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://walternascimentobarroso:CbXdwQyawLa4YDBy@wquiz.e6mk1np.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['quiz_database']
collection = db['quiz_collection']

@app.route('/')
def hello():
    return 'Hello, world!'

# Rotas da API
@app.route('/quiz', methods=['GET'])
def get_quiz():
    quiz_data = list(collection.find({}, {'_id': False}))
    return jsonify({"quiz": quiz_data})

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    submitted_answers = request.json.get("answers", [])

    # Aqui você pode comparar as respostas submetidas com as respostas corretas no banco de dados

    # Por exemplo, para simplificar, vamos apenas contar as respostas corretas
    score = sum(1 for submitted, correct in zip(submitted_answers, get_correct_answers()) if submitted == correct)

    return jsonify({"score": score})

@app.route('/quiz/add', methods=['POST'])
def add_quiz():
    new_question = request.json.get("question", {})
    collection.insert_one(new_question)
    return jsonify({"message": "Questão adicionada com sucesso!"})

def get_correct_answers():
    return [question["resposta_correta"] for question in collection.find({}, {"resposta_correta": 1, "_id": 0})]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

