# coding:utf8

# https://www.w3.org/Protocols/rfc2616/rfc2616.html
# https://flask-pymongo.readthedocs.io/en/latest/
# http://api.mongodb.com/python/current/api/pymongo/
# http://51elliot.blogspot.com.br/2014/04/rest-api-best-practices-http-and-crud.html
# http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# https://stackoverflow.com/questions/21411497/flask-jsonify-a-list-of-objects

from datetime import datetime, date
from bson import objectid, ObjectId
from bson.errors import InvalidId
# from bson.json_util import dumps
from flask import Flask, jsonify, render_template, request
from flask.json import JSONEncoder
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

# TODO transformar s saida em __str__()


class Character:
    def __init__(self, name, surname, birth_date, species, health, mana, gold_pieces, playable, game):
            self.mid = None
            self.name = name
            self.surname = surname
            self.birth_date = birth_date
            self.species = species
            self.health = health
            self.mana = mana
            self.gold_pieces = gold_pieces
            self.playable = playable
            self.game = game
            self.picture_path = 'static/img/'
            self.picture_file = name.lower() + '_' + surname.lower() + '.png'

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
                "picture_path": self.picture_path,
                "picture_file": self.picture_file
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
                "picture_path": c.picture_path,
                "picture_file": c.picture_file
            }}, upsert=True
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


class CharJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Character):
            print("entrou")
            return {
                "_id": o.mid,
                "name": o.name,
                "surname": o.surname,
                "birth_date": o.birth_date.date().isoformat(),
                "species": o.species,
                "health": o.health,
                "mana": o.mana,
                "gold_pieces": o.gold_pieces,
                "playable": o.playable,
                "game": o.game,
                "picture_path": o.picture_path,
                "picture_file": o.picture_file
            }
        return super(CharJSONEncoder, self).default(o)

app.json_encoder = CharJSONEncoder


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
        output = []
        for character in characters:
            output.append({
                "_id": character["_id"].__str__(),
                "name": character["name"],
                "surname": character["surname"],
                "birth_date": character["birth_date"].date().isoformat(),
                "species": character["species"],
                "health": character["health"],
                "mana": character["mana"],
                "gold_pieces": character["gold_pieces"],
                "playable": character["playable"],
                "game": character["game"],
                "picture_path": character["picture_path"],
                "picture_file": character["picture_file"]
            })

        # if OK, Return 200 OK
        return jsonify(output)
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
            return jsonify({'result': "400 Bad Request"})
        else:
            result = c.insert()
            return jsonify({'result': "201 Created"})


# GET /characters/12 - Retrieves a specific character
# PUT /characters/12 - Updates character #12
# PATCH /characters/12 - Partially updates character #12
# DELETE /characters/12 - Deletes character #12
@app.route('/characters/<char_id>', methods=['GET', 'PUT', 'DELETE'])
def character(char_id=None):
    """
    :GET (retrieve):\n
    :param char_id: The id of the character\n
    :returns: A json formatted representation of the character\n
    :URI example: /characters/592b837fddea8f224b48b28d\n
    :PUT (update):\n
    :param char_id: The id of the character\n
    :returns: If Update is OK, returns 200 OK. If it fails return
    :URI example: /characters/592b837fddea8f224b48b28d\n
    :DELETE:\n
    """
    try:
        # None if char  wasn't found
        char_id = ObjectId(char_id)
    except InvalidId as e:
        return jsonify("400 Bad Request", e.__str__())
    else:
        if request.method == 'GET':
            c = Character.retrieve_by_id(char_id)
            print("Char: ", c)
            if c is not None:
                # c['_id'] = c['_id'].__str__()
                # c['birth_date'] = c['birth_date'].date().isoformat()
                return jsonify("200 OK", c)
                # return jsonify(c)
            return jsonify("404 Not Found", c)

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
            result = c.update(char_id, c)
            print(result)
            print(result.acknowledged)
            print(result.raw_result)
            print(result.upserted_id)
            print(result.modified_count)
            print(result.matched_count)
            # c['_id'] = c['_id'].__str__()
            # c['birth_date'] = c['birth_date'].date().isoformat()
            output = jsonify("200 OK", c.retrieve_by_id(char_id))
            return output

        elif request.method == 'PATCH':
            pass
        elif request.method == 'DELETE':
            chars_collection.delete_one({'_id': char_id})
            output = jsonify({'result': "204 No content."})
            return output
    #     else:
    #         output = jsonify({'result': "404 Not Found. _id Not Found"})
    #         return output
    #
    # except Exception as e:
    #     print("Erro :", e, char_id)
    #     output = jsonify({'result': "400 bad request. Some Error whit the ID you passed."})
    #     return output




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
