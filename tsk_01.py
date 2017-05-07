# coding:utf8

from pymongo import MongoClient
from datetime import datetime


class Pessoa:
    def __init__(self, nome, sobrenome, idade, data_nascimento, salario, membro_ativo):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.salario = salario
        self.membro_ativo = membro_ativo

    # crud
    def insert(self):
        result = db.pessoa.insert_one(
            {
                "nome": self.nome,
                "sobrenome": self.sobrenome,
                "idade": self.idade,
                "data_nascimento": datetime.strptime(self.data_nascimento, "%d-%m-%Y"),
                "salario": self.salario,
                "membro_ativo": self.membro_ativo
            }
        )
        return result

    def read_by_name(self):
        cursor = db.pessoa.find({'nome': self.nome})
        return cursor

    def update(self):
        pass

    def delete_pessoa(self):
        r = db.pessoa.delete_many({'nome': self.nome})
        print(r.deleted_count)


if __name__ == "__main__":
    # Cria objeto Pessoa
    pessoa = Pessoa("Jonatan", "Vianna", 35, "20-07-1981", 60000.0, True)

    # instancia Mongo client com os parametros de conexão, (sem pswd e user)
    client = MongoClient('localhost', 27017)

    # Objeto Database <class 'pymongo.database.Database'>
    db = client.pessoa

    # Insert Pessoa
    pessoa.insert()

    #pessoa.delete_pessoa()

    c = db.pessoa.find()
    for i in c:
        print(i)






