# coding:utf8


from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo, ASCENDING


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'people'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/people'

#  https://flask-pymongo.readthedocs.io/en/latest/
mongo = PyMongo(app)

# client = MongoClient('mongodb://127.0.0.1:27017')
# db = client.people


class Person:
    def __init__(self, name, surname, id_number, birth_date, salary, associate):
        self.name = name
        self.surname = surname
        self.id_number = id_number
        self.birth_date = birth_date
        self.salary = salary
        self.associate = associate

    # crud
    def insert(self):
        insert_result = mongo.db.people.insert_one(
            {
                "name": self.name,
                "surname": self.surname,
                "id_number": self.id_number,
                "birth_date": datetime.strptime(self.birth_date, "%Y-%m-%d"),
                "salary": self.salary,
                "associate": self.associate
            }
        )
        return insert_result

    def read_by_name(self):
        cursor = mongo.db.people.find_one({'name': self.name})
        return cursor

    @staticmethod
    def update_by_name(name, new_name):
        update_result = mongo.db.people.update_one({"nome": name}, {"$set": {"nome": new_name}})
        return update_result

    def delete_by_name(self):
        delete_result = mongo.db.people.delete_one({'name': self.name})
        return delete_result

    @staticmethod
    def fill_in_db():
        # Creates object Person
        p0 = Person("Celes", "Chere", 100, "1990-07-07", 50000.0, True)
        p1 = Person("Kefka", "Palazzo", 101, "1975-08-05", 50000.0, False)
        p2 = Person("Locke", "Cole", 102, "1991-05-07", 50000.0, False)
        p3 = Person("Sabin", "Figaro", 103, "1983-01-29", 50000.0, False)
        p4 = Person("Edgar", "Figaro", 104, "1981-09-30", 50000.0, True)
        p5 = Person("Cyan", "Garamonde", 105, "1973-12-01", 50000.0, True)
        p6 = Person("Setzer", "Gabbiani", 106, "1981-07-20", 50000.0, False)
        p7 = Person("Relm", "Arrowny", 107, "2005-07-20", 50000.0, True)
        p8 = Person("Stragus", "Magus", 108, "1950-03-30", 50000.0, True)
        p9 = Person("Tina", "Branford", 109, "1999-10-18", 50000.0, True)

        person_list = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]

        # ------------------  Insert each Person -------------------
        for i in person_list:
            i.insert()

    def __str__(self):
        return"Name: {} {}\n" \
              "Birth Date: {}\n" \
              "ID Number: {}\n" \
              "Salary {}\n" \
              "Associate {}".format(self.name, self.surname, self.birth_date,
                                    self.id_number, self.salary, ("Yes" if self.associate else "No"))


@app.route('/', methods=['GET'])
def get_all_person():
    a = mongo.db.people.find().sort([('name', ASCENDING)])
    for b in a:
        print('{name}'.format(name=b['name']))

    cursor = mongo.db.people.find().sort([('name', ASCENDING)])
    out = []

    for people in cursor:
        out.append({'name': people['name'],
                    'surname': people['surname'],
                    'id_number': people['id_number'],
                    'birth_date': people['birth_date'],  # .strftime("%Y/%m/%d"),
                    'salary': people['salary'],
                    'associate': 'Yes' if people['associate'] else 'No'
                    })

    # return jsonify({'result': out})
    return render_template('people.html', people=out)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)

    # ------ Code for using only PyMongo Examples ----------

    # instanciates Mongo client with connection parameters, (no pswd and user)
    # client = MongoClient('localhost', 27017)

    # Objetc Database <class 'pymongo.database.Database'>
    # db = client.people

    # Person.fill_in_db()

    # Update Example
    # u = p2.update_by_name("Jonatan", "Celes")

    # Read
    # print(p2.read_by_name())

    # Delete
    # p3.delete_by_name()

    # c = mongo.db.people.find()
    # for i in c:
    #     print(i)
