# coding:utf8

from pymongo import MongoClient
from datetime import datetime


class Pessoa:
    def __init__(self, nome, sobrenome, matricula, data_nascimento, salario, socio):
        self.nome = nome
        self.sobrenome = sobrenome
        self.matricula = matricula
        self.data_nascimento = data_nascimento
        self.salario = salario
        self.socio = socio

    # crud
    def insert(self):
        insert_result = db.pessoa.insert_one(
            {
                "nome": self.nome,
                "sobrenome": self.sobrenome,
                "matricula": self.matricula,
                "data_nascimento": datetime.strptime(self.data_nascimento, "%d-%m-%Y"),
                "salario": self.salario,
                "socio": self.socio
            }
        )
        return insert_result

    def read_by_name(self):
        cursor = db.pessoa.find_one({'nome': self.nome})
        return cursor

    @staticmethod
    def update_by_name(nome, novo_nome):
        update_result = db.pessoa.update_one({"nome": nome}, {"$set": {"nome": novo_nome}})
        return update_result

    def delete_by_name(self):
        delete_result = db.pessoa.delete_one({'nome': self.nome})
        return delete_result

    def __str__(self):
        return"Nome: {} {}\n" \
              "Nascimento: {}\n" \
              "Matricula: {}\n" \
              "Salario {}\n" \
              "Socio {}".format(self.nome, self.sobrenome, self.data_nascimento,
                                self.matricula, self.salario, ("Sim" if self.socio else "Não"))


if __name__ == "__main__":
    # Cria objeto Pessoa
    p1 = Pessoa("Ronnie", "James Dio", 30001, "10-07-1942", 100000.0, True)
    p2 = Pessoa("Celes", "Chere", 20001, "20-07-1989", 70000.0, True)
    p3 = Pessoa("Kefka", "Palazzo", 10001, "20-07-1980", 50000.0, False)

    # instancia Mongo client com os parametros de conexão, (sem pswd e user)
    client = MongoClient('localhost', 27017)

    # Objeto Database <class 'pymongo.database.Database'>
    db = client.pessoa

    # Insert Pessoas
    # p1.insert()
    # p2.insert()
    # p3.insert()

    # Update
    # u = p2.update_by_name("Jonatan", "Celes")

    # Read
    # print(p2.read_by_name())

    # Delete
    p3.delete_by_name()

    c = db.pessoa.find()
    for i in c:
        print(i)
