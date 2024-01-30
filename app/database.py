from pymongo import MongoClient
from pymongo.server_api import ServerApi

class Database:
    def __init__(self, uri, db_name='quiz_database', collection_name='quiz_collection'):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_quiz_data(self):
        return list(self.collection.find({}, {'_id': False}))

    def insert_question(self, question):
        self.collection.insert_one(question)

    def get_correct_answers(self):
        return [question["resposta_correta"] for question in self.collection.find({}, {"resposta_correta": 1, "_id": 0})]
