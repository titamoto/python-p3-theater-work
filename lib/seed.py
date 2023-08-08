from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Audition, Role

fake = Faker()

engine = create_engine('sqlite:///theater.db')
Session = sessionmaker(bind=engine)
session = Session()

audition = [Audition(actor = fake.name(), location = fake.address(), phone = fake.random_int(5030000, 5039999), hired = fake.boolean(chance_of_getting_true = (100/3))) for i in range(30)]
role = [Role(character_name = fake.name()) for i in range(10)]

def delete_records():
    session.query(Audition).delete()
    session.query(Role).delete()
    session.commit()

def create_records():
    session.add_all(audition + role)
    session.commit()
    return audition, role

def relate_records(audition, role):
    for aud in audition:
        aud.role = rc(role)

    session.add_all(audition)
    session.commit()

if __name__ == '__main__':
    delete_records()
    audition, role = create_records()
    relate_records(audition, role)
