
from bson import json_util
from flask import Flask, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
chars_collection = client.game_characters.characters

app = Flask(__name__)
api = Api(app)

json_util.DEFAULT_JSON_OPTIONS.datetime_representation = json_util.DatetimeRepresentation.ISO8601
json_util.DEFAULT_JSON_OPTIONS.json_mode = 1

class Character(Resource):
    def get(self):
        result = chars_collection.find({})
        l = []
        for i in result:
            l.append(i)
        return json_util.dumps(result)

api.add_resource(Character, '/')

if __name__ == '__main__':
    app.run(debug=True)
