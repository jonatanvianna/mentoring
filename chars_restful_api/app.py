import json
from bson import json_util, ObjectId
from flask import Flask, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient, cursor, collection

client = MongoClient('mongodb://127.0.0.1:27017')
chars_collection = client.game_characters.characters

app = Flask(__name__)
api = Api(app)

json_util.DEFAULT_JSON_OPTIONS.datetime_representation = json_util.DatetimeRepresentation.ISO8601
json_util.DEFAULT_JSON_OPTIONS.json_mode = 1


class Character(Resource):
    def get(self, characters=None):
        if characters:
            # result is a Cursor class object, has tools to work with the query results
            result = chars_collection.find({"_id": ObjectId(characters)})
            # collection.Collection.find_one() returns a dict object
        else:
            result = chars_collection.find()
        l = []
        for i in result:
            l.append(i)
        return json.loads(json_util.dumps({'result': l})), 200, {'Etag': 'some-opaque-string'}

api.add_resource(Character,
                 '/',  # Get all Chars
                 '/oid/<string:oid>', endpoint="char_oid"
                 )

if __name__ == '__main__':
    app.run(debug=True, port=8000)
