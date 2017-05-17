# coding: utf-8
from pymongo import MongoClient


class Student:
    def __init__(self, name, undergrad, units, classes):
        self.name = name  # String
        self.undergrad = undergrad  # boolean
        self.units = units  # int
        self.classes = classes  # list ['geography', 'math', 'journalism']

    def insert(self):
        insert_result = db.student.insert_one(
            {
                "name": self.name,
                "undergrad": self.undergrad,
                "units": self.units,
                "classes": self.classes
            }
        )
        return insert_result

client = MongoClient('localhost', 27017)
db = client.examples

s1 = Student('Joe', True, 9, ['geography', 'math', 'journalism'])
s2 = Student('Jane', False, 12, ['geography', 'science', 'journalism', 'history'])
s3 = Student('Kevin', True, 3, ['geography'])
s4 = Student('Rachel', False, 6, ['geography', 'history'])

#s1.insert()
#s2.insert()
#s3.insert()
#s4.insert()

r = db.student.find({'classes': {'$in': ['history']}})
print(r)

for i in r:
    print(i)




