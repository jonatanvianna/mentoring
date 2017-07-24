# coding: utf-8

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://127.0.0.1:27017')
mongo = client['restbd']


@app.route('/star/<name>', methods=['GET'])
def get_one_star(name):
    s = mongo.stars.find_one({'name': name})
    if s:
        output = {'name': s['name'], 'distance': s['distance']}
    else:
        output = "No such name" 
    return jsonify({'result': output})


@app.route('/', methods=['GET'])
def hello_world():
    return "Surprise Motherfocka"


@app.route('/all_stars/', methods=['GET'])
def get_all_stars():
    star = mongo.stars.find()
    print(star)
    output = []
    print(type(star))
    for s in star:
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.stars
    name = request.json['name']
    print(name)
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    print(star_id)
    new_star = star.find_one({'_id': star_id})
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
