# coding:utf8

from pymongo import MongoClient
from datetime import datetime
import Flask

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
        insert_result = db.person.insert_one(
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
        cursor = db.person.find_one({'name': self.name})
        return cursor

    @staticmethod
    def update_by_name(name, new_name):
        update_result = db.person.update_one({"nome": name}, {"$set": {"nome": new_name}})
        return update_result

    def delete_by_name(self):
        delete_result = db.person.delete_one({'name': self.name})
        return delete_result

    def __str__(self):
        return"Name: {} {}\n" \
              "Birth Date: {}\n" \
              "ID Number: {}\n" \
              "Salary {}\n" \
              "Associate {}".format(self.name, self.surname, self.birth_date,
                                    self.id_number, self.salary, ("Yes" if self.associate else "No"))


if __name__ == "__main__":
    # Creates object Person
    p1 = Person("Ronnie", "James Dio", 30001, "1942-07-10", 100000.0, True)
    p2 = Person("Celes", "Chere", 20001, "1988-07-20", 70000.0, True)
    p3 = Person("Kefka", "Palazzo", 10001, "1980-07-20"
                                           ""
                                           "", 50000.0, False)

    # instanciates Mongo client with connection parameters, (no pswd and user)
    client = MongoClient('localhost', 27017)

    # Objetc Database <class 'pymongo.database.Database'>
    db = client.person

    # Insert each Person
    p1.insert()
    p2.insert()
    p3.insert()

    # Update Example
    # u = p2.update_by_name("Jonatan", "Celes")

    # Read
    # print(p2.read_by_name())

    # Delete
    # p3.delete_by_name()

    c = db.person.find()
    for i in c:
        print(i)
