# coding:utf8


from datetime import datetime
from flask import Flask, jsonify, render_template, request
from bson.json_util import dumps
from flask_pymongo import PyMongo, ASCENDING
# from pymongo import MongoClient


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'game_characters'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/game_characters'

#: https://flask-pymongo.readthedocs.io/en/latest/
mongo = PyMongo(app)

# client = MongoClient('mongodb://127.0.0.1:27017')
# mongo = client.game_characters


class Character:
    def __init__(self, name, surname, birth_date, species, health, mana, gold_pieces, playable, game):
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


# @app.route('/fill_in_db/', methods=['GET'])
def fill_in_db():
    # Creates objects Characters
    c0 = Character("Celes", "Chere", "1990-07-07", "Human", 9999, 9999, 50000.0, True, 'FFVI')
    c1 = Character("Kefka", "Palazzo", "1975-08-05", "Human", 9999, 9999, 666000.0, False, 'FFVI')
    c2 = Character("Locke", "Cole", "1991-05-07", "Human", 9999, 9999, 1000.0, False, 'FFVI')
    c3 = Character("Sabin", "Figaro", "1983-01-29", "Human", 9999, 9999,  900.0, False, 'FFVI')
    c4 = Character("Edgar", "Figaro", "1981-09-30", "Human", 9999, 9999,  4000.0, True, 'FFVI')
    c5 = Character("Cyan", "Garamonde", "1973-12-01", "Human", 9999, 9999,  89000.0, True, 'FFVI')
    c6 = Character("Setzer", "Gabbiani", "1981-07-20", "Human", 9999, 9999,  90000.0, False, 'FFVI')
    c7 = Character("Relm", "Arrowny", "2005-07-20", "Human", 9999, 9999,  4000.0, True, 'FFVI')
    c8 = Character("Stragus", "Magus", "1950-03-30", "Human", 9999, 9999,  70000.0, True, 'FFVI')
    c9 = Character("Tina", "Branford", "1999-10-18", "Esper", 9999, 9999,  60000.0, True, 'FFVI')
    char_list = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]

    # ------------------  Insert each Person -------------------

    if char_list:
        for i in char_list:
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
    all_chars = mongo.db.characters.find().sort([('name', ASCENDING)])
    output = []
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
            "game": characther["game"]
        })

    return jsonify({'result': output})
    # return jsonify({'result': dumps(all_chars)})
    # return render_template('characters.html', characters=output)


@app.route('/character/<name>', methods=['GET'])
def character(name=None):
    if name and request.method == 'GET':
        characther = mongo.db.characters.find({'name': name})
        
        output = {
                '_id': characther['_id'].__str__(),
                'name': characther['name'],
                'surname': characther['surname'],
                'birth_date': characther['birth_date'],
                'species': characther['species'],
                'health': characther['health'],
                'mana': characther['mana'],
                'gold_pieces': characther['gold_pieces'],
                'playable': characther['playable'],
                'game': characther['game']
        }

        return jsonify({'result': output})
        # return jsonify({'result': dumps(all_char)})


@app.route('/character', methods=['POST'])
def create_characther():
    """ Json Format for insert character
    
    {
        "name":"Jonatan",
        "surname":"Kopichenko",
        "birth_date": "1981-07-20",
        "species": "Human",
        "health": 9999,
        "mana": 9999,
        "gold_pieces": 7000.0,
        "playable": true,
        "game": "Life"
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
        'game': request.json['game']
    })
    return "User inserted in DB: " + insert_result.__str__()



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
