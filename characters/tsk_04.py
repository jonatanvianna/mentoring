# coding:utf8

# https://www.w3.org/Protocols/rfc2616/rfc2616.html
# https://flask-pymongo.readthedocs.io/en/latest/
# http://api.mongodb.com/python/current/api/pymongo/
# http://51elliot.blogspot.com.br/2014/04/rest-api-best-practices-http-and-crud.html
# http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


# BSON X JSON
# http://api.mongodb.com/python/current/api/bson/json_util.html
# https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable#
# https://stackoverflow.com/documentation/pymongo/9348/converting-between-bson-and-json#t=201710082232030056851

from datetime import datetime
from time import sleep
from bson import ObjectId
from bson.errors import InvalidId
from bson import json_util
from bson.json_util import DEFAULT_JSON_OPTIONS
from flask import Flask, jsonify, render_template, request, Response
from flask_pymongo import PyMongo, ASCENDING, DESCENDING
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'game_characters'
# app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/game_characters'

# Bridges Flask and Mongo
# mongo = PyMongo(app)

# CORS to prevent cross domain erros
CORS(app)

# to use without Flask-PyMongo
client = MongoClient('mongodb://127.0.0.1:27017')
chars_collection = client.game_characters.characters

# json_util datetime config
DEFAULT_JSON_OPTIONS.datetime_representation = json_util.DatetimeRepresentation.ISO8601
DEFAULT_JSON_OPTIONS.json_mode = 1
CHAR_IMG_PATH = 'static/img/'


class Character:
    def __init__(self, name, surname, birth_date, species, health, mana, gold_pieces, playable, game):
            self.id = ObjectId()
            self.name = name
            self.surname = surname
            self.birth_date = birth_date
            self.species = species
            self.health = health
            self.mana = mana
            self.gold_pieces = gold_pieces
            self.playable = playable
            self.game = game


    def insert(self):
        insert_result = chars_collection.insert_one({
                "name": self.name,
                "surname": self.surname,
                "birth_date": self.birth_date,
                "species": self.species,
                "health": self.health,
                "mana": self.mana,
                "gold_pieces": self.gold_pieces,
                "playable": self.playable,
                "game": self.game,
        })

        return insert_result

    @staticmethod
    def update(char_id, c):
        update_result = chars_collection.update_one(
            {"_id": char_id},
            {"$set": {
                "name": c.name,
                "surname": c.surname,
                "birth_date": c.birth_date,
                "species": c.species,
                "health": c.health,
                "mana": c.mana,
                "gold_pieces": c.gold_pieces,
                "playable": c.playable,
                "game": c.game,
                # upsert (optional): If True, perform an insert if no documents match the filter.
            }}, upsert=False
        )
        return update_result

    def retrieve_by_name(self):
        cursor = chars_collection.find_one({'name': self.name})
        return cursor

    @staticmethod
    def retrieve_by_id(char_id):
        r = chars_collection.find_one({'_id': char_id})
        return r

    @staticmethod
    def update_name(name, new_name):
        update_result = chars_collection.update_one({"nome": name}, {"$set": {"nome": new_name}})
        return update_result

    def delete_by_name(self):
        delete_result = chars_collection.delete_one({'name': self.name})
        return delete_result

    def create_file_name(self):
        self.picture_file = CHAR_IMG_PATH + self.name.lower() + '_' + self.surname.lower() + '_' + self.id.__str__() + '.png'


@app.route('/fill_in_db', methods=['GET'])
def fill_in_db():
    # Creates objects Characters
    c0 = Character("Celes", "Chere", datetime(1990, 7, 7), "Human", 9999, 9999, 50000.0, True, 'FFVI' )
    c1 = Character("Kefka", "Palazzo", datetime(1975, 8, 5), "Demi-God", 9999, 9999, 666000.0, False, 'FFVI')
    c2 = Character("Locke", "Cole", datetime(1991, 5, 7), "Human", 9999, 9999, 1000.0, True, 'FFVI')
    c3 = Character("Sabin", "Figaro", datetime(1983, 1, 29), "Human", 9999, 9999,  900.0, True, 'FFVI')
    c4 = Character("Edgar", "Figaro", datetime(1981, 9, 30), "Human", 9999, 9999,  4000.0, True, 'FFVI')
    c5 = Character("Cyan", "Garamonde", datetime(1973, 12, 1), "Human", 9999, 9999,  89000.0, True, 'FFVI')
    c6 = Character("Setzer", "Gabbiani", datetime(1981, 7, 20), "Human", 9999, 9999,  90000.0, True, 'FFVI')
    c7 = Character("Relm", "Arrowny", datetime(2005, 7, 20), "Human", 9999, 9999,  4000.0, True, 'FFVI')
    c8 = Character("Stragus", "Magus", datetime(1950, 3, 30), "Human", 9999, 9999,  70000.0, True, 'FFVI')
    c9 = Character("Tina", "Branford", datetime(1999, 10, 18), "Esper", 9999, 9999,  60000.0, True, 'FFVI')
    c10 = Character("Robo", "", datetime(2298, 7, 20), "Robot", 9999, 9999,  60000.0, True, 'Chrono Trigger')
    c11 = Character("Chrono", "", datetime(982, 1, 29), "Human", 9999, 9999,  60000.0, True, 'Chrono Trigger')

    char_list = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]

    # ------------------  Insert each Char -------------------

    if char_list:
        for i in char_list:
            print(i)
            i.insert()
        return "DB Filled"
    else:
        return "Error in fill DB"


# GET /tickets - Retrieves a list of tickets
# POST /tickets - Creates a new ticket
@app.route('/characters', methods=['GET', 'POST'])
def characters():
    """
    :GET:\n
    :URI example:/characters
    :returns: a list o json formatter representation of all characters
    :POST:\n
    :URI example:/characters
    :param : Json Format for insert character
             {
                 "name":"Celes",
                 "surname":"Chere",
                 "birth_date": "1981-07-20",
                 "species": "Human",
                 "health": 9999,
                 "mana": 9999,
                 "gold_pieces": 7000.0,
                 "playable": true,
                 "game": "Life",
             }"""
    if request.method == 'GET':
        characters = chars_collection.find().sort([('species', ASCENDING)])
        print(type(characters))
        result = []
        for char in characters:
            result.append(char)
        return Response(response=json_util.dumps({'result': result}), mimetype='application/json', status=200)
        # return json_util.dumps({'result': result})

    elif request.method == 'POST':
        try:
            c = Character(
                request.json['name'],
                request.json['surname'],
                datetime.strptime(request.json['birth_date'], '%Y-%m-%d'),
                request.json['species'],
                request.json['health'],
                request.json['mana'],
                request.json['gold_pieces'],
                request.json['playable'],
                request.json['game']
            )
        except Exception as e:
            print(e)
            return Response(response=json_util.dumps({'result': e.__str__()}), mimetype='application/json', status=400)
        else:
            result = c.insert()
            return Response(response=json_util.dumps({'result': "201 Created"}), mimetype='application/json', status=201)


# GET /characters/12 - Retrieves a specific character
# PUT /characters/12 - Updates character #12
# PATCH /characters/12 - Partially updates character #12
# DELETE /characters/12 - Deletes character #12
@app.route('/characters/<char_id>', methods=['GET', 'PUT', 'DELETE'])
def character(char_id=None):
    """
    :GET (retrieve):\n
    :param: char_id The id of the character\n
    :returns: A json formatted representation of the character and 200 OK.\n
              If not found, 404 NOT FOUND.\n
              If bad oid is passed, the error and a 400 BAD REQUEST.
    :URI example: /characters/592b837fddea8f224b48b28d\n

    :PUT (update):\n
    :param: char_id The id of the character\n
    :returns: If Update is OK, returns 200 OK. If not found 404. If bad oid is passed, returns 400.
    :URI example: /characters/592b837fddea8f224b48b28d\n
    :DELETE:\n
    """
    try:
        # char_id receives None if character wasn't found
        char_id = ObjectId(char_id)
    except InvalidId as e:
        return Response(response=json_util.dumps({'result': e.__str__()}), mimetype='application/json', status=400)
    except TypeError as e:
        return Response(response=json_util.dumps({'result': e.__str__()}), mimetype='application/json', status=400)
    else:
        if request.method == 'GET':
            c = Character.retrieve_by_id(char_id)
            if c is not None:
                return Response(response=json_util.dumps({'result': c}), mimetype='application/json', status=200)
            return Response(json_util.dumps({'result': c}), mimetype='application/json', status=404)

        elif request.method == 'PUT':
            c = Character(
                 request.json['name'],
                 request.json['surname'],
                 datetime.strptime(request.json['birth_date'], '%Y-%m-%d'),
                 request.json['species'],
                 request.json['health'],
                 request.json['mana'],
                 request.json['gold_pieces'],
                 request.json['playable'],
                 request.json['game'],
            )
            # http://api.mongodb.com/python/current/api/pymongo/results.html?highlight=updateresult#pymongo.results.UpdateResult
            result = c.update(char_id, c)
            if result.matched_count == 0:
                return Response(response=json_util.dumps({'return': {'matched_count': result.matched_count}}),
                                mimetype='application/json', status=404)
            elif result.modified_count == 1:
                return Response(response=json_util.dumps({'result': {'modified_count': result.modified_count}}),
                                mimetype='application/json', status=200)
            elif result.modified_count == 0:
                return Response(response=json_util.dumps({'result': {'modified_count': result.modified_count}}),
                                mimetype='application/json', status=201)

        elif request.method == 'PATCH':
            pass
        elif request.method == 'DELETE':
            result = chars_collection.delete_one({'_id': char_id})

            if result.deleted_count == 1:
                return Response(response=jsonify({'result': {'deleted_count': result.deleted_count}}),
                                mimetype='application/json', status=204)
            elif result.deleted_count == 0:
                return Response(response=jsonify({'result': {'deleted_count': result.deleted_count}}),
                                mimetype='application/json', status=404)


if __name__ == "__main__":
    app.run(debug=True)

    # ------ Code for using only PyMongo Examples ----------

    # Character.fill_in_db()

    # Update Example
    # u = p2.update_by_name("Jonatan", "Celes")

    # Retrieve
    # c = Character.retrieve_by_id()
    # print(jsonify(c))

    # Delete
    # p3.delete_by_name()

    # c = mongo.db.characters.find()
    # for i in c:
    #     print(i)
