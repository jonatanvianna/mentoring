# coding:utf8


from datetime import datetime, date
from bson import objectid, ObjectId
from bson.errors import InvalidId
from bson import json_util
from flask import Flask, jsonify, render_template, request
from flask.json import JSONEncoder
from flask_pymongo import PyMongo, ASCENDING, DESCENDING
from pymongo import MongoClient
from flask_cors import CORS
from marshmallow import Schema, fields, pprint


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
            self.picture_path = 'static/img/'
            self.picture_file = name.lower() + '_' + surname.lower() + '.png'

    @staticmethod
    def retrieve_by_name(name):
        cursor = chars_collection.find_one({'name': name})
        return cursor


class CharSchema(Schema):
    _id = fields.Integer()
    name = fields.Str()
    surname = fields.Str()
    birth_date = fields.DateTime()
    species = fields.Str()
    health = fields.Integer()
    mana = fields.Integer()
    gold_pieces = fields.Float()
    playable = fields.Boolean()
    game = fields.Str()
    picture_path = fields.Str()
    picture_file = fields.Str()

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


# c0 = Character("Celes", "Chere", datetime(1990, 7, 7), "Human", 9999, 9999, 50000.0, True, 'FFVI')

# c0 = Character.retrieve_by_name("Jonatan")
c0 = Character.retrieve_by_name("Celes")

# schema = CharSchema()
# result = schema.dumps(c0)
result = json_util.dumps(c0)
pprint(result)






