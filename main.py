import pprint
import os
import sqlalchemy as sa
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "Pessoas"
    cpf = Column("cpf", String, primary_key=True)
    primeiro_nome = Column("primeiro_nome", String)
    ultimo_nome = Column("ultimo_nome", String)
    idade = Column("idade", Integer)
    genero = Column("genero", CHAR)

    def __init__(self, cpf, primeiro_nome, ultimo_nome, genero, idade):
        self.cpf = cpf
        self.primeiro_nome = primeiro_nome
        self.ultimo_nome = ultimo_nome
        self.genero = genero
        self.idade = idade

    def __repr__(self):
        # return {
        #     "cpf":self.cpf, 
        #     "primeiro_nome": self.primeiro_nome,
        #     "ultimo_nome": self.ultimo_nome,
        #     "genero": self.ultimo_nome,
        #     "idade": self.idade
        # }
        return f'cpf:{self.cpf}, primeiro_nome: {self.primeiro_nome}, ultimo_nome: {self.ultimo_nome}, genero: {self.ultimo_nome}, idade: {self.idade}'

class Filho(Base):
    __tablename__ = "Filhos"
    tid = Column("id", Numeric, primary_key=True)
    nome_completo = Column("nome_completo", String)
    cpf_pai = Column(String, ForeignKey("Pessoas.cpf")) 

    def __init__(self, tid, nome, pai):
        self.tid = tid
        self.nome_completo = nome
        self.cpf_pai = pai

    def __repr__(self):
        return f'id: {self.tid}, nome_completo: {self.nome_completo}, pai: {self.cpf_pai}'

engine = create_engine("sqlite:///agenda.db", echo=True)
insp = sa.inspect(engine)

if not os.path.isfile("agenda.db"):
    Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

p1 = Pessoa(fake.ssn(),fake.first_name(),fake.last_name(),fake.random_letter(),fake.random_int(min=18, max=86))
session.add(p1)

filhos_p1 = [
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf)
]
session.add_all(filhos_p1)
session.commit()

p2 = Pessoa(fake.ssn(),fake.first_name(),fake.last_name(),fake.random_letter(),fake.random_int(min=18, max=86))
filhos_p2= [
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf)
]

p3 = Pessoa(fake.ssn(),fake.first_name(),fake.last_name(),fake.random_letter(),fake.random_int(min=18, max=86))
filhos_p3= [
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf)
]

p4 = Pessoa(fake.ssn(),fake.first_name(),fake.last_name(),fake.random_letter(),fake.random_int(min=18, max=86))
filhos_p4= [
    Filho(fake.random_number(), fake.name(), p1.cpf),
    Filho(fake.random_number(), fake.name(), p1.cpf)
]

session.add(p2)
session.add(p3)
session.add(p4)

session.add_all(filhos_p2)
session.add_all(filhos_p3)
session.add_all(filhos_p4)

session.commit()

# resultados = session.query(Pessoa).all()
# resultados = session.query(Pessoa.idade < 30)
# resultados = session.query(Pessoa).filter(Pessoa.idade < 30)

resultados = session.query(Filho, Pessoa).filter(Filho.cpf_pai == Pessoa.cpf).all()
print(f'TIPO DE RETORNO: -----------> {type(resultados)}')

for item in resultados:
    print(item.__repr__())