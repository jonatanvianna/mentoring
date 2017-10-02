# coding:utf8

from datetime import datetime
from bson import objectid, ObjectId
from flask import Flask, jsonify, render_template, request
# from bson.json_util import dumps
from flask_pymongo import PyMongo  # , ASCENDING
# from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'game_characters'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/game_characters'

#: https://flask-pymongo.readthedocs.io/en/latest/
mongo = PyMongo(app)
#: CORS tp precent erros of cross domain
CORS(app)

# client = MongoClient('mongodb://127.0.0.1:27017')
# mongo = client.game_characters


class Character:
    def __init__(self, name, surname, birth_date, species, health, mana, gold_pieces, playable, game, picture_path, picture_file):
            self.name = name
            self.surname = surname
            self.birth_date = birth_date
            self.species = species
            self.health = health
            self.mana = mana
            self.gold_pieces = gold_pieces
            self.playable = playable
            self.game = game
            self.picture_path = picture_path
            self.picture_file = picture_file

    def insert(self):
        insert_result = mongo.db.characters.insert_one({
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

    def read_by_name(self):
        cursor = mongo.db.characters.find_one({'name': self.name})
        return cursor

    @staticmethod
    def update_by_name(name, new_name):
        update_result = mongo.db.characters.update_one({"nome": name}, {"$set": {"nome": new_name}})
        return update_result

    def delete_by_name(self):
        delete_result = mongo.db.characters.delete_one({'name': self.name})
        return delete_result


@app.route('/fill_in_db/', methods=['GET'])
def fill_in_db():
    # Creates objects Characters
    c0 = Character("Celes", "Chere", "1990-07-07", "Human", 9999, 9999, 50000.0, True, 'FFVI', 'static/img/', 'celes_chere.png')
    c1 = Character("Kefka", "Palazzo", "1975-08-05", "Demi-God", 9999, 9999, 666000.0, False, 'FFVI', 'static/img/', 'kefka_palazzo.png')
    c2 = Character("Locke", "Cole", "1991-05-07", "Human", 9999, 9999, 1000.0, True, 'FFVI', 'static/img/', 'locke_cole.png')
    c3 = Character("Sabin", "Figaro", "1983-01-29", "Human", 9999, 9999,  900.0, True, 'FFVI', 'static/img/', 'sabin_figaro.png')
    c4 = Character("Edgar", "Figaro", "1981-09-30", "Human", 9999, 9999,  4000.0, True, 'FFVI', 'static/img/', 'edgar_figaro.png')
    c5 = Character("Cyan", "Garamonde", "1973-12-01", "Human", 9999, 9999,  89000.0, True, 'FFVI', 'static/img/', 'cyan_garamonde.png')
    c6 = Character("Setzer", "Gabbiani", "1981-07-20", "Human", 9999, 9999,  90000.0, True, 'FFVI', 'static/img/', 'setzer_gabbiani.png')
    c7 = Character("Relm", "Arrowny", "2005-07-20", "Human", 9999, 9999,  4000.0, True, 'FFVI', 'static/img/', 'relm_arrowny.png')
    c8 = Character("Stragus", "Magus", "1950-03-30", "Human", 9999, 9999,  70000.0, True, 'FFVI', 'static/img/', 'stragus_magus.png')
    c9 = Character("Tina", "Branford", "1999-10-18", "Esper", 9999, 9999,  60000.0, True, 'FFVI', 'static/img/', 'tina_brandford.png')
    char_list = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]

    # ------------------  Insert each Char -------------------

    if char_list:
        for i in char_list:
            print(i)
            i.insert()
        return "DB Filled"
    else:
        return "Error in fill DB"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name="World"):
    return render_template('hello.html', name=name)


@app.route('/', methods=['GET'])
def get_all_characters():
    all_chars = mongo.db.characters.find()#.sort([('name', ASCENDING)])
    output = []

    for character in all_chars:
        output.append({
            "_id": character["_id"].__str__(),
            "name": character["name"],
            "surname": character["surname"],
            "birth_date": character["birth_date"],
            "species": character["species"],
            "health": character["health"],
            "mana": character["mana"],
            "gold_pieces": character["gold_pieces"],
            "playable": character["playable"],
            "game": character["game"],
            "picture_path": character["picture_path"],
            "picture_file": character["picture_file"]
        })
    return jsonify(output)


@app.route('/character/<name>', methods=['GET'])
def character(name=None):
    """Accepts 'name' or '_id' to realize the query
        pattern: /character/Celes
        pattern: /character/592b837fddea8f224b48b28d
    """
    output = []
    if name:
        try:
            # _id = ObjectId(name)
            all_chars = mongo.db.characters.find({'name': name})
        except Exception as e:
            print(e)
            output = jsonify({'result': "Some Error in find the name."})
            # all_chars = mongo.db.characters.find({'name': name})
        else:
            if all_chars.count() > 1:
                for characther in all_chars:
                    output.append({
                        "_id": characther["_id"].__str__(),
                        "name": characther["name"],
                        "surname": characther["surname"],
                        'birth_date': characther['birth_date'],
                        'species': characther['species'],
                        'health': characther['health'],
                        'mana': characther['mana'],
                        'gold_pieces': characther['gold_pieces'],
                        "playable": characther["playable"],
                        "game": characther["game"],
                        "picture_path": character['picture_path'],
                        "picture_file": character['picture_file']
                    })
                output = "No Results Found"
            elif all_chars.count() == 1:
                for char in all_chars:
                    output = {
                        "_id": char["_id"].__str__(),
                        "name": char["name"],
                        "surname": char["surname"],
                        'birth_date': char['birth_date'],
                        'species': char['species'],
                        'health': char['health'],
                        'mana': char['mana'],
                        'gold_pieces': char['gold_pieces'],
                        "playable": char["playable"],
                        "game": char["game"],
                        "picture_path": char['picture_path'],
                        "picture_file": char['picture_file']
                    }

            else:
                output = "No Results Found"
        finally:
            return jsonify(output)
    else:
        return jsonify({'result': "Empty request."})


@app.route('/character', methods=['POST'])
def create_characther():
    """ Json Format for insert character
    
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
        "picture_path": "/static/img/"
        "picture_file": "celes_chere.png"
    }"""
    insert_result = mongo.db.characters.insert_one({
        'name': request.json['name'],
        'surname': request.json['surname'],
        'birth_date': datetime.strptime(request.json['birth_date'], '%Y-%m-%d'),
        'species': request.json['species'],
        'health': request.json['health'],
        'mana': request.json['mana'],
        'gold_pieces': request.json['gold_pieces'],
        'playable': request.json['playable'],
        'game': request.json['game'],
        'picture_path': request.json['picture_path'],
        'picture_file': request.json['picture_file']
    })

    return "User inserted in DB: " + insert_result.__str__()


@app.route('/character/<_id>', methods=['POST'])
def update_characther(_id=None):
    """ Json Format for update character

    {
        "name":"Celes",
        "surname":"Chere",
        "birth_date": "1981-07-20",
        "species": "Human",
        "health": "9999",
        "mana": "9999",
        "gold_pieces": "7000",
        "playable": "True",
        "game": "Life",
        "picture_path": "/static/img/celes_chere.png"
    }"""

    if _id:
        # {
        # < operator1 >: { < field1 >: < value1 >, ...},
        # < operator2 >: { < field2 >: < value2 >, ...},
        # ...
        # }
        # all_chars = mongo.db.characters.find({'_id': objectid(_id)})

        print(request.json['picture_path'])
        print(type(request.json['picture_path']))

        # print(_id)
        # r = mongo.db.characters.find({'_id': ObjectId(_id)})
        # for i in r:
        #     print(i)
        # print(r)

        all_chars = mongo.db.characters.find()

        for i in all_chars:
            print(i['name'])
            print(i['_id'])
            print(i['picture_path'])
            print(i['picture_file'])

        # result = mongo.db.characters.update_one(
        #     {'_id': ObjectId(_id)},
        #     {'$set':
        #          {
        #             'picture_path': request.json['picture_path'],
        #             'picture_file': request.json['picture_file']
        #          }
        #     },
        #     upsert=True
        # )
        # # result = mongo.db.characters.findAndModify({
        #     'query': {'_id': _id},
        #     'update': {
        #         {'$set': {'picture_path': request.json['picture_path']}}
        #     }
        # })
        #result = Character.update_by_name("Celes", request.json['name'])
        print(result)
        return "Entrou?"
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True)

    # ------ Code for using only PyMongo Examples ----------

    # Character.fill_in_db()

    # Update Example
    # u = p2.update_by_name("Jonatan", "Celes")

    # Read
    # print(p2.read_by_name())

    # Delete
    # p3.delete_by_name()

    # c = mongo.db.characters.find()
    # for i in c:
    #     print(i)
